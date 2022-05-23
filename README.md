# RADx Synthetic CDE Generation

## Purpose
Tools for generating synthetic CDE data intended for use within the RADx ecosystem.

## Installing
```bash
python3 -m venv venv
source ./venv/bin/activate
make install
```

## Tools

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

### Generating synthetic CDEs
Use a CDE template to generate synthetic CDE data.

```bash
python3 generate.py [-h] -t TEMPLATE -n ROW_COUNT [-o OUTPUT_PATH]
# or
make generate TEMPLATE=<template_file> ROW_COUNT=<rows_to_generate> OUTPUT_PATH="synthetic_cde_X.csv"
```