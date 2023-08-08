#!/usr/bin/env bash
set -ex

if [ -z "$1" ]; then
    echo "Usage: template_tier1.sh /path/to/data_dictionary_template.yaml"
    exit 1
fi

python template.py \
    --mapping_file="templating_data/Tier1_DataDictionary.csv" \
    --output_path="$1" \
    --mapping_file_delimiter="," \
    --name_column="Variable" \
    --responses_column="Responses" \
    --response_outer_delimiter=";" \
    --response_inner_delimiter=","