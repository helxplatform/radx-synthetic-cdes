import click
import csv
import yaml
from pathlib import Path
from _version import __version__

def generate_template_csv(mapping_file, output_path):
    """
    Generate a template file for CDE generation from a RADx CDE mapping file.
    :param mapping_file: File path to mapping file
    :type mapping_file: str
    :param output_path: Output path of the generated template file
    :type output_path: str
    """
    template = {
        "variables": {}
    }
    with open(mapping_file, "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        i = 0
        for row in reader:
            variable_template = []
            variable_name = row["Variable"]
            possible_responses = [
                # Split mapping into (value, name). Important to only split the first comma, since the name can also include commas
                # E.g. "0, No, not of Hispanic or Latino origin" -> ("0", "No, not of Hispanic or Latino origin")
                response.split(",", 1)
                # Split into individual variable mappings
                for response in row["Responses"].split(";")
            ]
            for possible_response in possible_responses:
                if len(possible_response) == 2:
                    # Normal response mapping of [value, name]
                    response_value, response_name = possible_response
                    response_name = response_name.strip()
                    response_value = int(response_value)
                    variable_template.append({
                        "response_name": response_name,
                        "response_value": response_value,
                        "frequency": None
                    })
                elif len(possible_response) == 1:
                    # User-input field, e.g. "text", "integer" -> user can enter any text or integer
                    response_type = possible_response[0].strip()
                    var_field = {
                        "response_name": response_type,
                        "response_value_generator": {},
                        "frequency": None
                    }
                    if response_type == "text":
                        # If lorem is specified, a lorem ipsum generator will be used.
                        var_field["response_value_generator"]["lorem"] = {
                            "num_sentences": [1, 4],
                            "sentence_length": [1, 50]
                        }
                        # If valid_inputs is specified, a random choice from the list will be used
                        var_field["response_value_generator"]["valid_inputs"] = None
                    if response_type == "integer":
                        # If range is specified, a random integer within the range will be used.
                        # If valid_inputs is specified, a random integer from the list will be used.
                        var_field["response_value_generator"]["range"] = [0, 0]
                        var_field["response_value_generator"]["valid_inputs"] = None
                    variable_template.append(var_field)

                    possible_responses = possible_responses[1:]
                else:
                    raise Exception(f"Parsing response with length {len(possible_response)} is not implemented. Response: {possible_response}")
            
            template["variables"][variable_name] = variable_template
    
    if Path(output_path).is_file():
        if not click.confirm(f"Template file already exists under \"{output_path}\". You will LOSE ALL DATA under the existing template. Continue anyways?"):
            print("Cancelled template generation.")
            return
    with open(output_path, "w+", encoding="utf-8") as out_file:
        out_file.write(f"""\
# Template generated using v{__version__}.
# Source mapping file: "{mapping_file}".
# 
# {len(template['variables'])} variables and {sum([len(template['variables'][variable]) for variable in template['variables']])} possible responses.
#
# Notes:
# - All responses under a variable with {{frequency: null}} will have the remaining frequency distribution divided evenly between them.
#   For example, a variable "nih_example" has four responses: foo{{frequency: 0.4}}, bar{{frequency: 0.3}}, egg{{frequency: null}}, spam{{frequency: null}}
#   At generation time, egg and spam will have the remaining 0.3 frequency divided evenly between them: egg{{frequency: 0.15}}, spam{{frequency: 0.15}}
# - Special responses: `text`, `integer`.
#   These responses do not have a preassigned "response_value" and require extra configuration to generate such a value.
#     integer:
#       // Choose between (prioritization: range > valid_inputs)
#       range: [min, max] // generates a random integer in inclusive range [min, max]
#       valid_inputs: int[] // chooses a random integer in list.
#     text:
#       // Choose between (prioritization: lorem > valid_inputs)
#       lorem: // generates random lorem ipsum text
#           num_sentences: [min, max] // number of sentences (inclusive range)
#           sentence_length: [min, max] // word length (inclusive range)
#       valid_inputs: str[] // chooses a random string in list.
# - For additional clarification on the structure of template files, refer to template_schema.json, which is the jsonschema specification
#   for template files.
""")
        yaml.safe_dump(template, out_file, allow_unicode=True, sort_keys=False)
    print(
        f"Generated new template file under \"{output_path}\" with {len(template['variables'])} variables " \
        f"and {sum([len(template['variables'][variable]) for variable in template['variables']])} possible responses."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create the base template file for CDE generation from a RADx CDE mapping file")
    parser.add_argument(
        "-m",
        "--mapping_file",
        help="RADx CDE mapping file, e.g. the RADx global cookbook",
        action="store",
        required=True
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="Output path of template file",
        action="store",
        default="cde_template.yaml"
    )

    args = parser.parse_args()
    mapping_file = args.mapping_file
    output_path = args.output_path

    generate_template_csv(mapping_file, output_path)