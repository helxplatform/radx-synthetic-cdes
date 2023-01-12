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
Alternatively, use a DataDictionary Mapping file (e.g `templating_data/RADxUP_DataDictionary_2022-10-24.csv`)
to create a template for generating CDE data.
- Templates configure how CDE data should be generated (response frequency, open-ended response generation, etc.)

```bash
python3 template.py [-h] -m MAPPING_FILE [-o OUTPUT_PATH]
# or
make template RADX_TEMPLATE_FILE=<mapping_file> OUTPUT_PATH="cde_template.yaml"
# or
make template-global-cookbook OUTPUT_PATH="cde_template.yaml"
```

## Template configuration

### Row count, relationships, & output file path
The `row_count` and `output_path` options can be used to configure how many records of data to generate and where to output the synthetic CDE file. The `relationships` option can be used to point towards a relationship configuration file used during generation (see Section: Relationships).
```yaml
row_count: <number_of_records_to_generate>
output_path: <output_file_name_or_path>
relationships: <relationship_file_name_or_path>
variables:
    ...
```

The top-level keys `row_count`, `relationships`, and `output_path` will be used by default in the absence of their respective cli arguments by the generation script.

### Frequency
The primary form of configuration in a template is the `frequency` key under each response. This should be between `0` and `1`, and the sum of all response `frequency` keys for each variable should not exceed `1`. The remaining frequency for a variable will be distributed evenly to all responses that have `frequency: null`.

### Open-ended responses (text and integers)
Some variables allow for open-ended `text` and `integer` responses. There are a few additional configuration options for how to generate such a response. Under the `response_value_generator` key:
```yaml
udf: # custom generation using UDFs (see Section: UDFs)
    name: <udf_name>
    args: # required config arguments for the udf, may be omitted if the UDF takes no required args.
        - <udf_required_arg1>
        - ...
    kwargs:
        # optional config arguments for the udf, may be omited if the UDF takes no keyword args.
        # note that required args (under the `args` key) may instead be specified by name here.
        kwarg1: <kwarg1_value>
        ...
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

### Relationships & UDFs
Relationships and UDFs are similar concepts that are both used within templates to specialize the generation of data.

#### UDFs
UDFs, or user-defined functions, may be used to programatically generate data on special fields such as `text` and `integer`. For example, while a `range` may suffice for age generation, a UDF would be more suitable if one wanted to generate ages conforming to the actual age distribution of the United States.

For reference on how to create UDFs, see `relationships/udfs.py`. Simply use the `@udf(name)` decorator from `relationships/register.py` and make sure the UDF is imported within `relationships/__init__.py`. A UDF can take arguments and keyword arguments for configuration and should return a value.
```python
from random import randint
from .register import udf

@udf("custom_age_generator")
def age_generator(min_age, max_age):
    """ Return a number in the inclusive range [min_age, max_age]. """
    return randint(min_age, max_age)
```

A UDF can then be used for a special-valued response (`text`, `integer`) within its `response_value_generator` field:
```yaml
nih_age:
    - response_name: text
      response_value_generator:
        udf:
          name: custom_age_generator
          kwargs:
            min_age: 18
            max_age: 100
      frequency: .95
...
```

#### Relationships
Relationships can be used to modify the generation of fields that depend on the values of other fields. Essentially, they are a specialized form of a UDF which modifies the selection of responses themselves, rather than the value of an already selected response (as is done in a regular UDF).

A basic example of a relationship would involve the disability variables found in the RADx global cookbook. If the response for `nih_disability` is "No", then the disability fields `nih_blind`, `nih_deaf`, `nih_memory`, `nih_walk_climb`, `nih_dress_bathe`, `nih_errand` should all be "Skip Logic".

Another example would be something such as age-associated diseases. As `nih_age` increases, the "Yes" response for variables such as `nih_alz` should become more likely (Alzheimer's is age-associated, i.e. its onset becomes more likely with age).

For reference on how to create relationships, see `relationships/relationships.py`. Use the `@relationship(name, dependencies, modifies)` decorator from `relationships/register.py` and make sure that the relationship is imported within `relationships/__init__.py`.
- The decorator requires you to specify `dependencies`, as in what the relationship needs to read, and `modifies`, as in what responses the relationship can modify, in order to construct a plan for generation order.

A relationship's first argument is always `responses`, which corresponds to the selected responses for the current record. The function can only read the responses specified in `dependencies`. The relationship should return modified responses.
```python
@relationship(
    name="no_disability",
    dependencies=[
        "nih_disability"
    ],
    modifies=[
            "nih_deaf",
            "nih_blind"
    ]
)
def my_custom_relationship(responses):
    nih_disability = responses["nih_disability"]
    if nih_disability["response_name"] == "No":
        return {
            "nih_deaf": {
                "response_name": "Skip Logic"
            },
            "nih_blind": {
                "response_name": "Skip Logic"
            }
        }

```

It can then be configured like so inside a relationships file:
```yaml
relationships:
  - name: no_disability
    # Note that args/kwargs can be omitted if the relationship doesn't use them.
    args: []
    kwargs: {}
  ...
```