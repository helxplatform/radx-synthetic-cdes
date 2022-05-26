# RADx Synthetic CDE Generation

## Purpose
Tools for generating synthetic CDE data intended for use within the RADx ecosystem.

## Installing
```bash
python3 -m venv venv
source ./venv/bin/activate
make install
```
Alternatively, for a quick in dirty install, you can just run `pip3 install -r requirements.txt`

## Quick start
```bash
pip3 install -r requirements.txt
python3 generate.py --row_count 1000 --output_path my_synthetic_cde.csv
...
Generated synthetic CDE file under "my_synthetic_cde.csv" with 1000 rows and 133 variables.
```

## Tools

### Generating synthetic CDEs
Use a CDE template (e.g. `cde_template.yaml`) to generate synthetic CDE data.

Running `generate.py` directly through a file browser/etc. will use `cde_template.yaml` as the template file and expects this template to specify `row_count`.

Alternatively:
```bash
python3 generate.py [-h] -t TEMPLATE -n ROW_COUNT [-o OUTPUT_PATH]
# or
make generate TEMPLATE=<template_file> ROW_COUNT=<rows_to_generate> OUTPUT_PATH="synthetic_cde_X.csv"
```

### Creating CDE templates
Use a RADx mapping file (e.g. `templating_data/radx_global_cookbook.csv`) to create a template for generating CDE data.
- Templates configure how CDE data should be generated (response frequency, open-ended response generation, etc.)

```bash
python3 template.py [-h] -m MAPPING_FILE [-o OUTPUT_PATH]
# or
make template RADX_TEMPLATE_FILE=<mapping_file> OUTPUT_PATH="cde_template.yaml"
# or
make template-global-cookbook OUTPUT_PATH="cde_template.yaml"
```

## Template configuration

### Row count & output file path
These options can be used to configure how many records of data to generate and where to output the synthetic CDE file.
```yaml
row_count: <number_of_records_to_generate>
output_path: <output_file_name_or_path>
variables:
    ...
```

The top-level keys `row_count` and `output_path` will be used by default in the absence of their respective cli arguments by the generation script.

### Frequency
The primary form of configuration in a template is the `frequency` key under each response. This should be between `0` and `1`, and the sum of all response `frequency` keys for each variable should not exceed `1`. The remaining frequency for a variable will be distributed evenly to all responses that have `frequency: null`.

### Open-ended responses (text and integers)
Some variables allow for open-ended `text` and `integer` responses. There are a few additional configuration options for how to generate such a response. Under the `response_value_generator` key:
```yaml
lorem: # for textual responses
    num_sentences: # inclusive
        - min
        - max
    sentence_length: # inclusive
        - min
        - max
range: # for integer responses
    # inclusive
    - min
    - max
valid_inputs: # for any type of response
    - this is a valid response
    - this is also a valid response
    ...
```
Only one of these fields should be specified for a response, and others should either be omitted or set to null.