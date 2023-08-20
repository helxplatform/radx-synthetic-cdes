import ruamel.yaml as yaml
import csv
import random
import os
from typing import NamedTuple, TypedDict, Union, List, Dict, Tuple, Any
from importlib.machinery import SourceFileLoader
from datetime import datetime
from pathlib import Path
from lorem.text import TextLorem
from relationships import Register

DEFAULT_CDE_OUTPUT_NAME = f"synthetic_datadictionary_{datetime.now().strftime('%m-%d-%Y')}"

class ResponseTemplate(TypedDict):
    response_name: str
    response_value: Union[int, str]
    response_value_generator: Union[Dict, None]
    frequency: Union[int, None]

class Response(TypedDict):
    response_name: str
    response_value: Union[int, str]

class Template(TypedDict):
    row_count: Union[int, None]
    output_path: Union[str, None]
    survey_cases: Union[str, None]
    case: Union[str, None]
    relationships: Union[List, None]
    udfs: Union[List, None]

    variables: List[ResponseTemplate]

class RelationshipTemplate(TypedDict):
    name: str
    args: Union[List[Any], None]
    kwargs: Union[Dict[str, Any], None]

class RelationshipsTemplate(TypedDict):
    relationships: List[RelationshipTemplate]

class SurveyCaseConfig(NamedTuple):
    valid_cases: List[str]
    default_disabled_response: ResponseTemplate
    survey_variables_config: Dict[str, Dict[str, Union[bool, ResponseTemplate]]]

def save_cde(cde_header, cde_rows, output_path):
    """
    Save the generated CDE file to a csv file.
    :param cde: Generated CDE data
    :type cde: list
    :param output_path: Output path of the generated synthetic CDE file
    :type output_path: str
    """
    i = 0
    while output_path is None:
        path = Path(f"{DEFAULT_CDE_OUTPUT_NAME}_{str(i)}.csv")
        if not path.is_file():
            output_path = str(path)
        i += 1


    csv_rows = [[cde_row[variable] for variable in cde_header] for cde_row in cde_rows]
    cde_csv = [cde_header] + csv_rows

    with open(os.path.join(os.path.dirname(__file__), output_path), "w+") as out_file:
        writer = csv.writer(out_file, delimiter=",")
        for row in cde_csv:
            writer.writerow(row)

def process_response_template(selected_response: ResponseTemplate) -> Response:
    # This function assumes that required UDFs have already been loaded into the Register
    selected_response_name = selected_response.get("response_name")
    selected_response_value = selected_response.get("response_value")
    generator_schema = selected_response.get("response_value_generator")
    if generator_schema is not None:
        udf = generator_schema.get("udf")
        lorem = generator_schema.get("lorem")
        range_ = generator_schema.get("range")
        valid_inputs = generator_schema.get("valid_inputs")
        if udf is not None:
            name = udf["name"]
            args = udf.get("args", [])
            kwargs = udf.get("kwargs", {})
            selected_response_value = Register.invoke_udf(name, *args, **kwargs)
        elif lorem is not None:
            min_sentences, max_sentences = lorem["num_sentences"] # inclusve
            min_words, max_words = lorem["sentence_length"] # inclusive
            lorem = TextLorem(srange=(min_words, max_words))
            sentences = [lorem.sentence() for i in range(random.randint(min_sentences, max_sentences))]
            selected_response_value = " ".join(sentences) # sentences automatically end in periods.
        elif range_:
            min_val, max_val = range_ # inclusive
            selected_response_value = random.randint(min_val, max_val)
        elif valid_inputs:
            selected_response_value = random.choice(valid_inputs)
    
    return Response(
        response_name=selected_response_name,
        response_value=selected_response_value
    )

def preprocess_template(template: Template):
    for variable_name in template["variables"]:
        responses = template["variables"][variable_name]
        no_freq_responses = []
        total_freq = 0
        for response in responses:
            if response.get("frequency") is None:
                no_freq_responses.append(response)
            else:
                total_freq += response["frequency"]
        if total_freq > 1:
            print(Exception(f"Sum of response frequencies for variable \"{variable_name}\" should not exceed 1.0 (total_freq={total_freq})"))
        if len(no_freq_responses) > 0:
            remaining_freq = 1 - total_freq
            per_response_freq = remaining_freq / len(no_freq_responses)
            # Due to floating-point imprecision, this will result in very slightly less or more than 1.0 total frequency,
            for response in no_freq_responses:
                response["frequency"] = per_response_freq

def generate_rows(template: Template, case: str, survey_case_config: SurveyCaseConfig, relationships: RelationshipsTemplate, row_count: int):
    header_row = list(template["variables"].keys())
    rows = [{variable: None for variable in header_row} for i in range(row_count)]
    for variable_name in template["variables"]:
        responses = template["variables"][variable_name]
        selected_responses = random.choices(
            responses,
            weights=[response["frequency"] for response in responses],
            k=row_count
        )
        for i in range(row_count):
            selected_response = selected_responses[i]
            response = process_response_template(selected_response)
            rows[i][variable_name] = {
                "response_name": response["response_name"],
                "response_value": response["response_value"]
            }
    # After bulk generation is complete, go through and manually regenerate responses on each record using relationships.
    relationship_plan = Register.plan(relationships["relationships"])
    # for dependency_node in relationship_plan:
    print("Starting post-processing of records.")
    if len(relationship_plan) == 0:
        print("- No relationships loaded.")
    for relationship in relationship_plan:
        print(f'- Processing relationship: {relationship["name"]}')    
        for record in rows:
            modifications = Register.invoke_relationship(
                relationship,
                record
            )
            if modifications is None: continue
            for modified_variable in modifications:
                modified_response = modifications[modified_variable]
                # These are functionally equivalent, except for special responses (i.e. text), in which it is necessary to support both.
                response_name = modified_response.get("response_name")
                response_value = modified_response.get("response_value")
                response = None

                if response_name is not None and response_value is not None:
                    response = modified_response
                elif response_name is not None:
                    for res in template["variables"][modified_variable]:
                        if res["response_name"] == response_name:
                            response = res
                            break
                elif response_value is not None:
                    for res in template["variables"][modified_variable]:
                        if res["response_value"] == response_value:
                            response = res
                            break
                else:
                    raise Exception(f"Could not interpret modification requested by relationship. Response: {modified_response}; variable: {modified_variable}")
                
                if response is None:
                    raise Exception(f"Could not find response requested by relationship. Response: {modified_response}; variable: {modified_variable}")
#                 print(f'''\
# Relationship "{relationship["name"]}" modified variable {modified_variable}: changed {record[modified_variable]["response_name"]} -> {response["response_name"]}')\
# ''')
                record[modified_variable] = {
                    "response_name": response["response_name"],
                    "response_value": response["response_value"]
                }
        
    if survey_case_config:
        print(f"Modifying records according to format specified by survey case {case}")
        for record in rows:
            for variable in record:
                variable_case = survey_case_config.survey_variables_config.get(variable, {}).get(case, True)
                if variable_case == True or variable_case == "yes" or variable_case == "Yes":
                    # This variable is enabled on the survey. No modification required.
                    continue
                elif variable_case == False or variable_case == "no" or variable_case == "No":
                    # This variable is disabled on the survey. Use the default disabled response.
                    selected_response = survey_case_config.default_disabled_response
                else:
                    # This variable is disabled on the survey. Use the specified response.
                    selected_response = variable_case
                
                response = process_response_template(selected_response)
                record[variable] = {
                    "response_name": response["response_name"],
                    "response_value": response["response_value"]
                }
    
    return (header_row, [{variable: record[variable]["response_value"] for variable in record} for record in rows])
def generate_cde_case(
    template_file,
    template,
    relationships,
    row_count,
    survey_case_config,
    case,
    output_path
):
    preprocess_template(template)

    if row_count is None:
        row_count = template.get("row_count", None)
    # row_count is either not given in template or also `null`
    if row_count is None:
        raise Exception(f"""\
Please specify the `row_count` field in "{template_file}" (or the `--row_count` argument if using the command line). Ex:
# ...
# ...
row_count: <rows_to_generate>
output_path: ...
variables:
    ...\
""")
    if output_path is None:
        output_path = template.get("output_path", None)


    [cde_header, cde_rows] = generate_rows(template, case, survey_case_config, relationships, row_count)

    save_cde(cde_header, cde_rows, output_path)

    print(
        f"Generated synthetic CDE file under \"{output_path}\" with {row_count} rows and {len(cde_header)} variables using template \"{template_file}\"."
    )

def generate_cde(
    template_file,
    row_count,
    survey_cases=None,
    case=[],
    relationship_file=[],
    udf_file=[],
    output_path=None
):
    """
    Generate a synthetic CDE file from a template file.
    :param template_file: File path(s) to CDE generation template.
    :type template_file: str | List[str]
    :param row_count: Number of records to generate.
    :type row_count: int
    :param survey_cases: Path to template specifying which variables to include/exclude from the template for a given "survey". 
    :type survey_cases: str | None
    :param case: The specific survey case to use.
    :type case: str | List[str]
    :param udf_file: File path(s) to Python files defining UDFs used within template.
    :type udf_file: str | List[str]
    :param output_path: Output path of the generated synthetic CDE file
    :type output_path: str
    """
    template_file = os.path.join(os.path.dirname(__file__), template_file)
    with open(template_file, "r") as f:
        template = yaml.round_trip_load(f)

    # Use `survey_cases` from template if not specified by a CLI argument.
    if not survey_cases: survey_cases = template.get("survey_cases")
    # Use `case` from template if not specified by a CLI aargument
    if len(case) == 0: 
        case = template.get("case")
        if isinstance(case, str): 
            case = [case]

    survey_case_config = None
    if survey_cases:
        print(f"Loading survey case template file {survey_cases}")
        with open(os.path.join(os.path.dirname(template_file), survey_cases), "r") as f:
            survey_cases = yaml.round_trip_load(f)
            try:
                valid_cases = survey_cases["cases"]
            except: raise Exception(f"Please specify the `cases` field in \"{survey_cases}\"")

            try:
                default_disabled_response = survey_cases["default_disabled_response"]
            except: raise Exception(f"Please specify the `default_disabled_response` field in \"{survey_cases}\"")

            try:
                survey_variables_config = survey_cases["variables"]
            except: raise Exception(f"Please specify the `variables` field in \"{survey_cases}\"")
            
            survey_case_config = SurveyCaseConfig(
                valid_cases,
                default_disabled_response,
                survey_variables_config
            )
    
    if survey_cases and not case:
        raise Exception(
            f"""\
Survey cases provided but no case is specified.
Please specify the `case` field in "{template_file}" (or the `--case` argument if using the command line). Ex:
# ...
# ...
survey_cases: ...
case: {survey_case_config.valid_cases[0]}
variables:
    ...\
""")
    for _case in case:
        if _case not in survey_case_config.valid_cases:
            raise Exception(f"The specified case \"{_case}\" is not declared as a valid case: {survey_case_config.valid_cases}")


    template_udf_file = template.get("udfs")
    if template_udf_file:
        if not isinstance(template_udf_file, list): template_udf_file = [template_udf_file]
        udf_file += template_udf_file

    template_relationship_file = template.get("relationships")
    if template_relationship_file:
        if not isinstance(template_relationship_file, list): template_relationship_file = [template_relationship_file]
        relationship_file += template_relationship_file
    
    # Load UDFs
    for udf_f in udf_file:
        before_udf_count = len(Register.udfs)
        SourceFileLoader(
            udf_f,
            os.path.join(os.path.dirname(__file__), os.path.dirname(template_file), udf_f)
        ).load_module()
        print(f"Loaded {len(Register.udfs) - before_udf_count} UDFs into the register from {udf_f}")

    # Load relationships    
    relationships = {
        "relationships": []
    }
    for rel_file in relationship_file:
        with open(os.path.join(os.path.dirname(template_file), rel_file), "r") as f:
            data = yaml.round_trip_load(f)
            relationships["relationships"] += data["relationships"]

            before_relationship_count = len(Register.relationships)
            SourceFileLoader(
                data["file"],
                os.path.join(os.path.dirname(__file__), os.path.dirname(template_file), data["file"])
            ).load_module()
            print(f"Loaded {len(Register.relationships) - before_relationship_count} relationships into the register from {rel_file}")
    if len(case) != 0:
        for _case in case:
            [*out_name, ext] = output_path.split(".")
            out_name[0] += f"_case_{_case}"
            out_name = ".".join([*out_name, ext])

            generate_cde_case(
                template_file,
                template,
                relationships,
                row_count,
                survey_case_config,
                _case,
                out_name
            )
    else:
        generate_cde_case(
            template_file,
            template,
            relationships,
            row_count,
            survey_case_config,
            None,
            output_path
        )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic CDE file")
    parser.add_argument(
        "-t",
        "--template",
        help="CDE template specifying how to generate the mock CDE",
        action="store",
        default="config/global_codebook/cde_template_data_dictionary.yaml"
    )
    parser.add_argument(
        "-r",
        "--relationships",
        nargs="*",
        help="Template specifying specialized generation via variable relationships",
        action="store",
        default=[],
        required=False
    )
    parser.add_argument(
        "-u",
        "--udfs",
        nargs="*",
        help="Specify Python UDF definitions",
        action="store",
        default=[],
        required=False
    )
    parser.add_argument(
        "-s",
        "--survey_cases",
        help="""\
Template specifying which variables to include/exclude from the template for a given 'survey'. \
If no survey cases are specified, the entire template is treated as a single survey.""",
        action="store",
        required=False
    )
    parser.add_argument(
        "-c",
        "--case",
        nargs="*",
        help="The specific survey case to run from the survey cases template file",
        action="store",
        required=False,
        default=[]
    )
    parser.add_argument(
        "-n",
        "--row_count",
        help="Number of rows of synthetic CDE data to generate.",
        action="store",
        type=int,
        default=None
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="Output path of synthetic CDE file",
        action="store",
        default=None
    )

    args = parser.parse_args()
    template = args.template
    relationships = args.relationships
    udfs = args.udfs
    row_count = args.row_count
    survey_cases = args.survey_cases
    case = args.case
    output_path = args.output_path

    generate_cde(
        template,
        row_count,
        survey_cases,
        case,
        relationship_file=relationships,
        udf_file=udfs,
        output_path=output_path
    )