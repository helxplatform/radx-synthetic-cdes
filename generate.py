import yaml
import csv
import random
from datetime import datetime
from pathlib import Path
from lorem.text import TextLorem

DEFAULT_CDE_OUTPUT_NAME = f"synthetic_cde_{datetime.now().strftime('%m-%d-%Y')}"

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

    with open(output_path, "w+") as out_file:
        writer = csv.writer(out_file, delimiter=",")
        for row in cde_csv:
            writer.writerow(row)

    

def preprocess_template(template):
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
            raise Exception(f"Sum of response frequencies for variable \"{variable_name}\" should not exceed 1.0 (total_freq={total_freq})")
        if len(no_freq_responses) > 0:
            remaining_freq = 1 - total_freq
            per_response_freq = remaining_freq / len(no_freq_responses)
            # Due to floating-point imprecision, this will result in very slightly less or more than 1.0 total frequency,
            for response in no_freq_responses:
                response["frequency"] = per_response_freq

def generate_rows(template, row_count):
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
            selected_response_value = selected_response.get("response_value")
            generator_schema = selected_response.get("response_value_generator")
            if generator_schema is not None:
                # Special response type e.g. `text`, `integer`
                lorem = generator_schema.get("lorem")
                range_ = generator_schema.get("range")
                valid_inputs = generator_schema.get("valid_inputs")
                if lorem is not None:
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
            rows[i][variable_name] = selected_response_value
    
    return (header_row, rows)

def generate_cde(template_file, row_count, output_path=None):
    """
    Generate a synthetic CDE file from a template file.
    :param template_file: File path to CDE generation template.
    :type template_file: str
    :param output_path: Output path of the generated synthetic CDE file
    :type output_path: str
    """
    with open(template_file, "r") as f:
        template = yaml.safe_load(f)

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


    [cde_header, cde_rows] = generate_rows(template, row_count)

    save_cde(cde_header, cde_rows, output_path)

    print(
        f"Generated synthetic CDE file under \"{output_path}\" with {row_count} rows and {len(cde_header)} variables using template \"{template_file}\"."
    )


if __name__ == "__main__":
    import argparse
    import generate
    
    parser = argparse.ArgumentParser(description="Generate synthetic CDE file")
    parser.add_argument(
        "-t",
        "--template",
        help="CDE template specifying how to generate the mock CDE",
        action="store",
        default="cde_template.yaml"
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
    row_count = args.row_count
    output_path = args.output_path

    generate.generate_cde(template, row_count, output_path)