PYTHON       = /usr/bin/env python3
VERSION_FILE = ./_version.py
VERSION      = $(shell cut -d " " -f 3 ${VERSION_FILE})

TEMPLATE := cde_template_data_dictionary.yaml
# TEMPLATE2 := cde_template_data_dictionary.yaml
OUTPUT_PATH :=

.DEFAULT_GOAL = help
.PHONY = help clean install template template-global-cookbook generate

#help: List available tasks on this project
help:
	@grep -E '^#[a-zA-Z\.\-]+:.*$$' $(MAKEFILE_LIST) | tr -d '#' | awk 'BEGIN {FS = ": "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

#clean: Remove old build artifacts and installed packages
clean:
	${PYTHON} -m pip uninstall -y -r requirements.txt
	rm -rf __pycache__

#install: Install application along with required development packages
install:
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt

#template: Generate template for use in CDE generation.
template:
ifndef RADX_TEMPLATE_FILE
	$(error RADX_TEMPLATE_FILE not specified)
endif
	${PYTHON} template.py --mapping_file ${RADX_TEMPLATE_FILE} \
		$(if ${OUTPUT_PATH}, --output_path ${OUTPUT_PATH},)

# ifndef RADX_TEMPLATE_FILE
# 	$(error RADX_TEMPLATE_FILE not specified)
# endif
# 	${PYTHON} template_datadictionary.py --mapping_file ${RADX_TEMPLATE_FILE} \
# 		$(if ${OUTPUT_PATH}, --output_path ${OUTPUT_PATH},)

#template-global-cookbook: Generate CDE template using the global RADx cookbook data.
#template: Generate a CDE template using the Data Dictionary.

template-global-cookbook:
	${PYTHON} template.py --mapping_file templating_data/Tier1_Data_Dictionary.csv \
		$(if ${OUTPUT_PATH}, --output_path ${OUTPUT_PATH},)

template-global-datadictionary:
	${PYTHON} template_datadictionary.py --mapping_file templating_data/RADxUP_DataDictionary_2022-10-24.csv \
		$(if ${OUTPUT_PATH}, --output_path ${OUTPUT_PATH},)


#generate: Generate synthetic CDE data from a CDE template.
generate:
ifndef TEMPLATE
	$(error TEMPLATE not set (should point to a CDE template file))
endif
# ifndef ROW_COUNT
# 	$(error ROW_COUNT not set (determines how many rows of data to generate))
# endif
ifndef TEMPLATE
	${PYTHON} generate.py --template ${TEMPLATE} --row_count ${ROW_COUNT} \
		$(if ${OUTPUT_PATH}, --output_path2 ${OUTPUT_PATH},)
else TEMPLATE2
	${PYTHON} generate.py --template ${TEMPLATE2} --row_count ${ROW_COUNT} \
		$(if ${UTPUT_PATH}, --output_path ${OUTPUT_PATH},)
endif
