import click
import csv
import os
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq
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
        "row_count": 1000,
        "output_path": None,
        "variables": {}
    }
    with open(os.path.join(os.path.dirname(__file__), mapping_file), "r") as f:
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
                            "num_sentences": [1, 2],
                            "sentence_length": [1, 10]
                        }
                        # If valid_inputs is specified, a random choice from the list will be used
                        var_field["response_value_generator"]["valid_inputs"] = None
                    if response_type == "integer":
                        # If range is specified, a random integer within the range will be used.
                        # If valid_inputs is specified, a random integer from the list will be used.
                        var_field["response_value_generator"]["range"] = [0, 10]
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
    with open(os.path.join(os.path.dirname(__file__), output_path), "w+", encoding="utf-8") as out_file:
        document_comment = f"""\
Template generated using v{__version__}.
Source mapping file: "{mapping_file}".
#
{len(template['variables'])} variables and {sum([len(template['variables'][variable]) for variable in template['variables']])} possible responses.
#
Don't change any `response_name` or `response_value` values!
For responses, only `frequency` (and `response_value_generator` for text/integers) should be modified.
#
Notes:
- All responses under a variable with {{frequency: null}} will have the remaining frequency distribution divided evenly between them.
  For example, a variable "nih_example" has four responses: foo{{frequency: 0.4}}, bar{{frequency: 0.3}}, egg{{frequency: null}}, spam{{frequency: null}}
  At generation time, egg and spam will have the remaining 0.3 frequency divided evenly between them: egg{{frequency: 0.15}}, spam{{frequency: 0.15}}
- Special responses: `text`, `integer`.
  These responses do not have a preassigned "response_value" and require extra configuration to generate such a value.
    integer:
      // Choose between (prioritization: range > valid_inputs)
      range: [min, max] // generates a random integer in inclusive range [min, max]
      valid_inputs: int[] // chooses a random integer in list.
    text:
      // Choose between (prioritization: lorem > valid_inputs)
      lorem: // generates random lorem ipsum text
          num_sentences: [min, max] // number of sentences (inclusive range)
          sentence_length: [min, max] // word length (inclusive range)
      valid_inputs: str[] // chooses a random string in list.
- For additional clarification on the structure of template files, refer to template_schema.json, which is the jsonschema specification
  for template files.

"""
        yaml = ruamel.yaml.YAML()
        # Ensure that `None` is dumped as `null`.
        yaml.representer.add_representer(type(None), lambda self, data: self.represent_scalar('tag:yaml.org,2002:null', 'null'))
        # Makes list yaml more readable
        yaml.indent(sequence=4, offset=2)
        
        commented_yaml = CommentedMap(template)
        commented_yaml.yaml_set_start_comment(document_comment, indent=0)
        commented_yaml.yaml_set_comment_before_after_key(
            "row_count",
            "How many records of data to generate. If null, `generate.py` will expect [-n ROW_COUNT] argument to be specified.\n" \
            "Ex: `row_count: 1000` will generate 1000 records of data when the template is run.",
            indent=0
        )
        commented_yaml.yaml_set_comment_before_after_key(
            "output_path",
            "File name/path to output the data under (or `null` to auto-generate a name). Can be overriden by [-o OUTPUT_PATH] argument.\n" \
            "Ex: `output_path: my_synthetic_cde.csv` will output the synthetic CDE under `my_synthetic_cde.csv` when the template is run.",
            indent=0
        )

        for variable in commented_yaml["variables"]:
            commented_yaml["variables"][variable] = CommentedSeq(commented_yaml["variables"][variable])
            for i, response in enumerate(commented_yaml["variables"][variable]):
                commented_yaml["variables"][variable][i] = CommentedMap(commented_yaml["variables"][variable][i])
            for response in commented_yaml["variables"][variable]:
                # response.yaml_set_comment_before_after_key("frequency", "Change this!", indent=6)
                response.yaml_set_comment_before_after_key(
                    "response_value_generator",
                    "Requires special configuration.",
                    indent=6
                )
                if "response_value_generator" in response:
                    generator = CommentedMap(response["response_value_generator"])
                    response["response_value_generator"] = generator
                    generator.yaml_set_comment_before_after_key("lorem", "Generates pseudo-Latin text.", indent=8)
                    generator.yaml_set_comment_before_after_key("range", "Chooses a random integer in the inclusive range.", indent=8)
                    generator.yaml_set_comment_before_after_key(
                        "valid_inputs",
                        "Randomly chooses a value from the list. Ex: ['a', 'b', 'c'] or [1, 2, 3]",
                        indent=8
                    )
                    if "lorem" in generator:
                        generator["lorem"] = CommentedMap(generator["lorem"])
                        generator["lorem"]["num_sentences"] = CommentedSeq(generator["lorem"]["num_sentences"])
                        generator["lorem"]["sentence_length"] = CommentedSeq(generator["lorem"]["sentence_length"])

                        generator["lorem"]["num_sentences"].yaml_set_comment_before_after_key(0, "Minimum number of sentences", indent=12)
                        generator["lorem"]["num_sentences"].yaml_set_comment_before_after_key(1, "Maximum number of sentences", indent=12)

                        generator["lorem"]["sentence_length"].yaml_set_comment_before_after_key(0, "Minimum number of words per sentence", indent=12)
                        generator["lorem"]["sentence_length"].yaml_set_comment_before_after_key(1, "Maximum number of words per sentence", indent=12)
                    if "range" in generator:
                        generator["range"] = CommentedSeq(generator["range"])
                        generator["range"].yaml_set_comment_before_after_key(0, "Minimum value", indent=10)
                        generator["range"].yaml_set_comment_before_after_key(1, "Maximum value", indent=10)


        yaml.dump(commented_yaml, out_file)
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