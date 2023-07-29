from random import random, choice, choices, randint
import pandas as pd
from relationships.register import relationship
import random

"""
A relationship is a post-generation utility for correlating relationships between fields.
For example, an 80 year old is far more likely to have alzheimers than a 40 year old. This observation can be enforced via a relationship.

Detailed info regarding implementation found in readme. Basics are as follows:
- A relationship needs to be decorated with @relationship to be added to the register (and thus made available to yaml configuration files).
- @relationship takes the following:
    - name: what to reference the relationship under, used for various things like configuring its use in yaml.
    - dependencies: what variables the relationship depends on, as in what variables does the relationship have to read in order to determine its output. 
    - modifies: what variables the relationship modifies the results of.
- A relationship's first arg is always `responses` which is a full dict of { [variable_name]: chosen_response }. It is important
  that any variables accessed from `responses` are listed as dependencies.
- A relationship should output None or a dict of { [variable_name]: modified_response }. If a modified response's frequency is not specified,
  it is interpreted that the modified response *must* be chosen (similar to frequency: 1.0 but without conflicts arising from exceeding the 1.0 frequency limit).
"""

def lerp(a, b, t):
    return a + t * (b - a)

@relationship(
    name="no_consent",
    dependencies=[
        "consent_given"
    ],
    modifies=[
            "consent_mdy",
            "consent_ident",
            "consent_zip",
            "consent_recontact"
    ]
)
def no_consent(responses):
    radxup_consent_given = responses["consent_given"]
    if radxup_consent_given["response_name"] == "No":
        return {
            "consent_mdy": {
                "response_name": "Skip Logic"
            },
            "consent_ident": {
                "response_name": "Skip Logic"
            },
            "consent_zip": {
                "response_name": "Skip Logic"
            },
            "consent_recontact": {
                "response_name": "Skip Logic"
            }
        }


@relationship(
    name="race_ethn_race",
    dependencies=[
        "race_ethn_race"
    ],
    modifies=[
            "race_ethn_asian_detail_2"
    ]
)
def race_ethn_race(responses):
   race_ethn_race = responses["race_ethn_race"]
   if race_ethn_race["response_name"] == "1":
        return {
            "race_ethn_asian_detail_2": {
                "response_name": "3"
            }
        }

@relationship(
    name="race_ethn_race_islander",
    dependencies=[
        "race_ethn_race",
        "race_ethn_race_islander"
    ],
    modifies=[
            "race_ethn_islander_detail_2"
    ]
)
def race_ethn_islander(responses):
   race_ethn_race = responses["race_ethn_race_islander"]
   if race_ethn_race["response_name"] == "1":
        return {
            "race_ethn_islander_detail_2": {
                "response_name": "4"
            }
        }

@relationship(
    name="race_ethn_race",
    dependencies=[
        "race_ethn_race"
    ],
    modifies=[
        "race_ethn_hispanic"
    ]
)
def race_ethn_hispanic(responses):
   race_ethn_race = responses["race_ethn_race"]
   if race_ethn_race["response_name"] == "1":
        return {
            "race_ethn_hispanic": {
                "response_name": "15"
            }
        }


@relationship(
    name="positive_covid",
    dependencies=[
        "tested_for_covid"
    ],
    modifies=[
        "tested_positive_for_covid",
        "positivemonth_covidtest_2",
        "positiveyear_covidtest_3",
        "recentmonth_covidtest_2",
        "recentyear_covidtest_3",
        "recentresult_covidtest",
        "cov_tst_mthd_2"
    ]
)
def positive_covid(responses):
    positive_covid = responses["tested_for_covid"]
    if positive_covid["response_name"] == "0":
        return {
            "tested_positive_for_covid": {
                "response_name": "Skip Logic"
            },
            "positivemonth_covidtest_2": {
                "response_name": "Skip Logic"
            },
            "positiveyear_covidtest_3": {
                "response_name": "Skip Logic"
            },
            "recentmonth_covidtest_2": {
                "response_name": "Skip Logic"
            },
            "recentyear_covidtest_3": {
                "response_name": "Skip Logic"
            },
            "recentresult_covidtest": {
                "response_name": "Skip Logic"
            },
            "cov_tst_mthd_2": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="self_reported_height_coded",
    dependencies=[
        "self_reported_height_coded"
    ],
    modifies=[
        "height_feet",
        "height_inches",
        "height_meters",
        "height_centimeters"
    ]
)
def self_reported_height_coded(responses):
    radx_self_reported_height_coded = responses["self_reported_height_coded"]
    if radx_self_reported_height_coded["response_name"] == "2":
        return {
            "height_feet": {
                "response_name": "Skip Logic"
            },
            "height_inches": {
                "response_name": "Skip Logic"
            }
        }
    elif radx_self_reported_height_coded["response_name"] == "1":
         return {
            "height_meters": {
                "response_name": "Skip Logic"
            },
            "height_centimeters": {
                "response_name": "Skip Logic"
            }
        }
  
@relationship(
    name="self_reported_weight_units",
    dependencies=[
        "self_reported_weight_units"
    ],
    modifies=[
        "self_reported_weight_kgs",
        "self_reported_weight_lbs"
    ]
)
def self_reported_weight_units(responses):
    self_reported_weight_units = responses["self_reported_weight_units"]
    if self_reported_weight_units["response_name"] == "1":
        return {
            "self_reported_weight_lbs": {
                "response_name": "Skip Logic"
            }
        }
    elif self_reported_weight_units["response_name"] == "2":
         return {
            "self_reported_weight_kgs": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="vaccine_acceptance",
    dependencies=[
        "flu_vaccinehistind_2"
    ],
    modifies=[
        "flu_vaccine_season_3"
    ]
)
def vaccine_acceptance(responses):
    vaccine_acceptance = responses["flu_vaccinehistind_2"]
    if vaccine_acceptance["response_name"] != "1":
        return {
            "flu_vaccine_season_3": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="bio_sex_birth_2",
    dependencies=[
        "bio_sex_birth_2"
    ],
    modifies=[
        "pregnancy_status"
    ]   
)
def bio_sex_birth_2(responses):
    bio_sex_birth_2 = responses["bio_sex_birth_2"]
    if bio_sex_birth_2["response_name"] == "1":
        return {
            "pregnancy_status": {
                "response_name": "0"
            }
        }
    
@relationship(
    name="household_famgen_3",
    dependencies=[
        "household_famgen_3"
    ],
    modifies=[
        "household_homeless"
    ]
)
# added 1 as a place holder
def household_famgen_3(responses):
   household_famgen_3 = responses["household_famgen_3"]
   if household_famgen_3["response_name"] == "90":
        return {
            "race_ethn_hispanic": {
                "household_homeless": "1"
            }
        }

@relationship(
    name="household_homeless",
    dependencies=[
        "household_homeless"
    ],
    modifies=[
        "household_congregate_3"
    ]
)

# added 1 as a place holder
def household_homeless(responses):
    household_homeless = responses["household_homeless"]
    if household_homeless["response_name"] == "1":
        return {
            "household_congregate_3": {
                "response_name": "1"
            }
        }

@relationship(
    name="household_congregate_3",
    dependencies=[
        "household_congregate_3"
    ],
    modifies=[
        "household_other"
    ]
)

# added home as a place holder
def household_congregate_3(responses):
    household_congregate_3 = responses["household_congregate_3"]
    if household_congregate_3["response_name"] == "90":
        return {
            "household_other": {
                "response_name": "home"
            }
        }

@relationship(
    name="current_employment_status",
    dependencies=[
        "current_employment_status"
    ],
    modifies=[
        "cur_employ_stat_specify",
        "employed_ew",
        "employed_healthcare_2"
    ]
)

# added fillers 
def current_employment_status(responses):
    current_employment_status = responses["current_employment_status"]
    if current_employment_status["response_name"] != "96":
        return {
            "cur_employ_stat_specify": {
                "response_name": "home"
            }
        }
    elif current_employment_status["response_name"] == "1":
        return {
            "employed_ew": {
                "response_name": "1"
            },
             "employed_healthcare_2": {
                "response_name": "1"
             }
        }

@relationship(
    name="language_pref",
    dependencies=[
        "language_pref"
    ],
    modifies=[
        "language_pref_other"
    ]
)

# added fillers 
def language_pref(responses):
    language_pref = responses["language_pref"]
    if language_pref["response_name"] == "90":
        return {
            "language_pref_other": {
                "response_name": "9"
            }
        }

@relationship(
    name="current_employment_status",
    dependencies=[
        "current_employment_status"
    ],
    modifies=[
        "cur_employ_stat_specify",
        "employed_ew",
        "employed_healthcare_2"
    ]
)

# added fillers 
def current_employment_status(responses):
    current_employment_status = responses["current_employment_status"]
    if current_employment_status["response_name"] == "1":
        return {
            "employed_ew": {
                "response_name": "1"
            },
            "employed_healthcare_2": {
                "response_name": "1"
            },
        }
    elif current_employment_status["response_name"] == "96":
        return {
            "cur_employ_stat_specify": {
                "response_name": "9"
            }
        }
@relationship(
    name="household_homeless",
    dependencies=[
        "household_homeless",

    ],
    modifies=[
        "household_congregate_3"
    ]
)
# added fillers 
def household_homeless(responses):
    household_homeless_status = responses["household_homeless"]
    if household_homeless_status["response_name"] == "1":
        return {
            "household_congregate_3": {
                "response_name": "1"
            }
        }

@relationship(
    name="household_congregate_3",
    dependencies=[
        "household_congregate_3",
    ],
    modifies=[
        "household_other"
    ]
)
# added fillers 
def household_congregate_3(responses):
    household_congregate_3_status = responses["household_congregate_3"]
    if household_congregate_3_status["response_name"] == "90":
        return {
            "household_other": {
                "household_other": "1"
            }
        }
    
@relationship(
    name="take_presc_meds",
    dependencies= "take_presc_meds",
    modifies=[
        "name_of_rx_med1",
        "name_of_rx_med2",
        "name_of_rx_med3",
        "name_of_rx_med4",
        "name_of_rx_med5",
        "name_of_rx_med6",
        "name_of_rx_med7",
        "name_of_rx_med8",
        "name_of_rx_med9",
        "name_of_rx_med10",
        "name_of_rx_med11",
        "name_of_rx_med12",
        "name_of_rx_med13",
        "name_of_rx_med14",
        "name_of_rx_med15"
    ]
)
# added fillers 
def take_presc_meds(responses):
    take_presc_meds_status = responses["take_presc_meds"]
    if take_presc_meds_status["response_name"] == "No":
        return {
            "name_of_rx_med1": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med2": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med3": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med4": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med5": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med6": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med7": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med8": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med9": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med10": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med11": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med12": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med13": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med14": {
                "response_name": "Skip Logic"
            },
            "name_of_rx_med15": {
                "response_name": "Skip Logic"
            }
        }
    elif take_presc_meds_status["response_name"] == "Yes" :
        #relative path
        df = pd.read_csv('/Users/asiyahahmad/Documents/GitHub/radx-synthetic-cdes/drugs data - data.csv')
        drug_frequencies = list(df['Cumulative Percentage'].diff().fillna(df['Cumulative Percentage']))

        #generate a random number between 0 and 15
        num_drugs = random.randint(0, 15)
        #crugs = list(df['Drug To Use'])

        #choose 'num_drugs' randomly from the drugs list based on their drug frequencies
        chosen_drugs = random.choices(df['Drug To Use'], weights=drug_frequencies, k=num_drugs)

        #get the drug class for each chosen drug
        drug_classes = set()
        chosen_drugs_with_classes = []
        for drug in chosen_drugs:
            drug_class = df.loc[df['Drug To Use'] == drug, 'Drug Class'].iloc[0]
            if drug_class not in drug_classes:
                drug_classes.add(drug_class)
                chosen_drugs_with_classes.append((drug, drug_class))

        modified_responses = {}

        #loop through and set modified response to drug names
        for i, drug_name in enumerate(chosen_drugs, 1):
            response_key = f"name_of_rx_med{i}"
            modified_responses[response_key] = {
                "response_name": drug_name
            }

        #mark "Skip Logic" for values not in num_drugs
        for n in range(num_drugs + 1, 15):
            response_key = f"name_of_rx_med{n}"
            modified_responses[response_key] = {
                "response_name": "Skip Logic"
            }

        # Return modified_responses with drug names as response values
        return modified_responses