#!/usr/bin/env bash
set -ex

if [ -z "$1" ]; then
    echo "Usage: template_tier2.sh /path/to/data_dictionary_template.yaml"
    exit 1
fi

python template.py \
    --mapping_file="templating_data/Tier2_DataDictionaries/Tier2_DataDictionary_RADxUP.csv" \
    --output_path="$1" \
    --mapping_file_delimiter="," \
    --name_column="Variable / Field Name" \
    --responses_column="Choices, Calculations, OR Slider Labels" \
    --response_outer_delimiter="|" \
    --response_inner_delimiter=","