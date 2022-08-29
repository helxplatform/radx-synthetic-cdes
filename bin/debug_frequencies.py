import csv
import math
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Debug frequencies of responses in a synthetic CDE file")
    parser.add_argument(
        "file",
        help="File path to synthetic CDE file",
        action="store"
    )
    parser.add_argument(
        "-f",
        "--fields",
        nargs="+",
        help="CDE variable/response in format [<name>=<response_value?> ...]"
    )
    args = parser.parse_args()
    fp = args.file
    fields = args.fields

    with open(fp, "r") as f:
        rows = [r for r in csv.DictReader(f)]
    
    counts = {}

    for row in rows:
        for key in row:
            value = row[key]
            if not key in counts: counts[key] = {}
            if not value in counts[key]: counts[key][value] = 0
            counts[key][value] += 1
    
    for field in fields:
        val = field.split("=", 1)
        if len(val) == 1:
            variable = val[0]
            values = [[variable, response_value] for response_value in counts[variable]]
        else:
            values = [val]
        for value in values:
            variable, response_value = value
            count = counts[variable].get(response_value, 0)
            freq = math.ceil(count / len(rows) * 10000) / 100
            print(f"{variable}={response_value} appears at a {freq}% frequency ({count} occurences)")