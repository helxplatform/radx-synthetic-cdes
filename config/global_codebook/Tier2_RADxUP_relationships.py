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
        "employed_healthcare_2",
        "covid_pto"
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
            },
             "covid_pto": {
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
    name="current_employment_status",
    dependencies=[
        "current_employment_status",
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
    if current_employment_status["response_name"] == "96":
        return {
            "cur_employ_stat_specify": {
                "response_name": "1"
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
    name="test_for_covid",
    dependencies=[
        "test_for_covid"
    ],
    modifies=[
        "recentmonth_covidtest_2",
        "recentyear_covidtest_3",
        "recentresult_covidtest",
        "cov_tst_mthd_2",
        "tested_positive_for_covid"

    ]
)
# added fillers 
def test_for_covid(responses):
    test_for_covid = responses["test_for_covid"]
    if test_for_covid["response_name"] == "1":
        return {
            "recentmonth_covidtest_2": {
                "response_name" == "1"
            },
            "recentyear_covidtest_3": {
                "response_name" == "1"
            },
            "recentresult_covidtest": {
                "response_name" == "1"
            },
            "cov_tst_mthd_2": {
                "response_name" == "1"
            },
            "tested_positive_for_covid": {
                "response_name" == "1"
            }
        }
    
@relationship(
    name="tested_positive_for_covid",
    dependencies=[
        "tested_positive_for_covid",
    ],
    modifies=[
        "positivemonth_covidtest_2",
        "positivemonth_covidtest_2"
    ]
)
# added fillers 
def tested_positive_for_covid(responses):
    tested_positive_for_covid = responses["tested_positive_for_covid"]
    if tested_positive_for_covid["response_name"] == "90":
        return {
            "positivemonth_covidtest_2": {
                "response_name": "1"
            },
            "positivemonth_covidtest_2": {
                "response_name": "1"
            }
        }    
@relationship(
    name="covid_test_approval",
    dependencies=[
        "covid_test_approval",
    ],
    modifies=[
        "covid_test_approval_other"
    ]
)
# added fillers 
def covid_test_approval(responses):
    covid_test_approval = responses["covid_test_approval"]
    if covid_test_approval["response_name"] == "90":
        return {
            "covid_test_approval_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_collection_setting",
    dependencies=[
        "covid_test_collection_setting",
    ],
    modifies=[
        "cov_tst_col_set_oth"
    ]
)
# added fillers 
def covid_test_collection_setting(responses):
    covid_test_collection_setting = responses["covid_test_collection_setting"]
    if covid_test_collection_setting["response_name"] == "90":
        return {
            "cov_tst_col_set_oth": {
                "response_name": "1"
            }
        }    
@relationship(
    name="covid_test_performed_location",
    dependencies=[
        "covid_test_performed_location",
    ],
    modifies=[
        "cov_tst_perf_loc_oth"
    ]
)
# added fillers 
def covid_test_performed_location(responses):
    covid_test_performed_location = responses["covid_test_performed_location"]
    if covid_test_performed_location["response_name"] == "90":
        return {
            "cov_tst_perf_loc_oth": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_study_setting",
    dependencies=[
        "covid_test_study_setting",
    ],
    modifies=[
        "covid_test_study_setting_other"
    ]
)
# added fillers 
def covid_test_study_setting(responses):
    covid_test_study_setting = responses["covid_test_study_setting"]
    if covid_test_study_setting["response_name"] == "90":
        return {
            "covid_test_study_setting_other": {
                "response_name": "1"
            }
        }    
@relationship(
    name="covid_test_type",
    dependencies=[
        "covid_test_type",
    ],
    modifies=[
        "covid_test_type_other"
    ]
)
# added fillers 
def covid_test_type(responses):
    covid_test_type = responses["covid_test_type"]
    if covid_test_type["response_name"] == "90":
        return {
            "covid_test_type_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_type",
    dependencies=[
        "covid_test_type",
    ],
    modifies=[
        "covid_test_type_other"
    ]
)
# added fillers 
def covid_test_type(responses):
    covid_test_type = responses["covid_test_type"]
    if covid_test_type["response_name"] == "90":
        return {
            "covid_test_type_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_specimen_type",
    dependencies=[
        "covid_test_specimen_type",
    ],
    modifies=[
        "covid_test_specimen_type_other"
    ]
)
# added fillers 
def covid_test_specimen_type(responses):
    covid_test_specimen_type = responses["covid_test_specimen_type"]
    if covid_test_specimen_type["response_name"] == "90":
        return {
            "covid_test_specimen_type_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_specimen_collector",
    dependencies=[
        "covid_test_specimen_collector",
    ],
    modifies=[
        "cov_tst_spec_col_oth"
    ]
)
# added fillers 
def covid_test_specimen_collector(responses):
    covid_test_specimen_collector = responses["covid_test_specimen_collector"]
    if covid_test_specimen_collector["response_name"] == "90":
        return {
            "cov_tst_spec_col_oth": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_specimen_collector",
    dependencies=[
        "covid_test_specimen_collector",
    ],
    modifies=[
        "cov_tst_spec_col_oth"
    ]
)
# added fillers 
def covid_test_specimen_collector(responses):
    covid_test_specimen_collector = responses["covid_test_specimen_collector"]
    if covid_test_specimen_collector["response_name"] == "90":
        return {
            "cov_tst_spec_col_oth": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_test_result",
    dependencies=[
        "covid_test_result",
    ],
    modifies=[
        "covid_test_result_other"
    ]
)
# added fillers 
def covid_test_result(responses):
    covid_test_result = responses["covid_test_result"]
    if covid_test_result["response_name"] == "90":
        return {
            "covid_test_result_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="lifetime_use_alcohol",
    dependencies=[
        "lifetime_use_alcohol",
    ],
    modifies=[
        "alcohol_daysperweek"
    ]
)
# added fillers 
def lifetime_use_alcohol(responses):
    lifetime_use_alcohol = responses["lifetime_use_alcohol"]
    if lifetime_use_alcohol["response_name"] == "1":
        return {
            "alcohol_daysperweek": {
                "response_name": "1"
            }
        }    

@relationship(
    name="smoker_cur_stat_2",
    dependencies=[
        "smoker_cur_stat_2",
    ],
    modifies=[
        "smoker_number"
    ]
)
# added fillers 
def smoker_cur_stat_2(responses):
    smoker_cur_stat_2 = responses["smoker_cur_stat_2"]
    if smoker_cur_stat_2["response_name"] == "4":
        return {
            "smoker_number": {
                "response_name": "1"
            }
        }    
        
@relationship(
    name="sex_orient_id",
    dependencies=[
        "sex_orient_id",
    ],
    modifies=[
        "sex_orient_desc_2"
    ]
)

# added fillers 
def sex_orient_id(responses):
    sex_orient_id = responses["sex_orient_id"]
    if sex_orient_id["response_name"] == "96":
        return {
            "sex_orient_desc_2": {
                "response_name": "1"
            }
        }    

@relationship(
    name="sex_orient_desc_2",
    dependencies=[
        "sex_orient_desc_2",
    ],
    modifies=[
        "sex_orient_desc_other"
    ]
)
# added fillers 
def sex_orient_desc_2(responses):
    sex_orient_desc_2 = responses["sex_orient_desc_2"]
    if sex_orient_desc_2["response_name"] == "96":
        return {
            "sex_orient_desc_other": {
                "response_name": "1"
            }
        }    


@relationship(
    name="self_reported_disability",
    dependencies=[
        "self_reported_disability",
    ],
    modifies=[
        "disability_decisions_2",
        "disability_walking_2",
        "disability_dress_2",
        "disability_errands_2"
    ]
)
# added fillers 
def self_reported_disability(responses):
    self_reported_disability = responses["self_reported_disability"]
    if self_reported_disability["response_name"] == "1":
        return {
            "disability_decisions_2": {
                "response_name": "1"
            },
            "disability_walking_2": {
                "response_name": "1"
            },
            "disability_dress_2": {
                "response_name": "1"
            },
            "disability_errands_2": {
                "response_name": "1"
            },

        }    

@relationship(
    name="covid_vaccine",
    dependencies=[
        "covid_vaccine",
    ],
    modifies=[
        "disability_decisions_2",
        "disability_walking_2",
        "disability_dress_2",
        "disability_errands_2",
        "vaccine_manufac_2",
        "vaccine_dose",
        "vaccine_rec1_dte",
        "vaccine_last_dte",
        "vaccine_edu_pre",
        "vaccine_edu_post"
    ]
)
# added fillers 
def covid_vaccine(responses):
    covid_vaccine = responses["covid_vaccine"]
    if covid_vaccine["response_name"] == "1":
        return {
            "disability_decisions_2": {
                "response_name": "1"
            },
            "disability_walking_2": {
                "response_name": "1"
            },
            "disability_dress_2": {
                "response_name": "1"
            },
            "disability_errands_2": {
                "response_name": "1"
            },
            "vaccine_manufac_2": {
                "response_name": "1"
            },
            "vaccine_dose" : {
                "response_name": "1"
            },
            "vaccine_rec1_dte" : {
                "response_name": "1"
            },
            "vaccine_last_dte": {
                "response_name": "1"
            },
            "vaccine_edu_pre" : {
                "response_name": "1"
            },
            "vaccine_edu_post": {
                "response_name": "1"
            }

        }    

@relationship(
    name="covid_had",
    dependencies=[
        "covid_had",
    ],
    modifies=[
        "covid_risk"
    ]
)
# added fillers 
def covid_had(responses):
    covid_had = responses["covid_had"]
    if covid_had["response_name"] == "0":
        return {
            "covid_risk": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_tested_30",
    dependencies=[
        "covid_tested_30",
    ],
    modifies=[
        "covid_tst_reas"
    ]
)
# added fillers 
def covid_tested_30(responses):
    covid_tested_30 = responses["covid_tested_30"]
    if covid_tested_30["response_name"] == "1":
        return {
            "covid_tst_reas": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_tst_reas",
    dependencies=[
        "covid_tst_reas",
    ],
    modifies=[
        "covid_tst_reas_other"
    ]
)
# added fillers 
def covid_tst_reas(responses):
    covid_tst_reas = responses["covid_tst_reas"]
    if covid_tst_reas["response_name"] == "5":
        return {
            "covid_tst_reas_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="covid_tst_reas",
    dependencies=[
        "covid_tst_reas",
    ],
    modifies=[
        "covid_tst_reas_other"
    ]
)
# added fillers 
def covid_tst_reas(responses):
    covid_tst_reas = responses["covid_tst_reas"]
    if covid_tst_reas["response_name"] == "5":
        return {
            "covid_tst_reas_other": {
                "response_name": "1"
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
        df = pd.read_csv('/Users/asiyahahmad/Documents/GitHub/radx-synthetic-cdes/templating_data/drugs data - data.csv')
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

@relationship(
    name="lifetime_use_alcohol",
    dependencies=[
        "lifetime_use_alcohol"
    ],
    modifies=[
        "alcohol_drinksperday"
    ]
)
# added fillers 
def lifetime_use_alcohol(responses):
    lifetime_use_alcohol = responses["lifetime_use_alcohol"]
    if lifetime_use_alcohol["response_name"] == "1":
        return {
            "alcohol_drinksperday": {
                "response_name": "1"
            }
        }    

@relationship(
    name="lifetime_use_alcohol",
    dependencies=[
        "lifetime_use_alcohol"
    ],
    modifies=[
        "alcohol_drinksperday"
    ]
)
# added fillers 
def lifetime_use_alcohol(responses):
    lifetime_use_alcohol = responses["lifetime_use_alcohol"]
    if lifetime_use_alcohol["response_name"] == "1":
        return {
            "alcohol_drinksperday": {
                "response_name": "1"
            }
        }    

@relationship(
    name="comp_thrombosis",
    dependencies= "comp_thrombosis",
    modifies=[
        "comp_thromb_location"
    ]
)
# added fillers 
def comp_thrombosis(responses):
    comp_thrombosis = responses["comp_thrombosis"]
    if comp_thrombosis["response_name"] == "1":
        return {
            "comp_thromb_location": {
                "response_name": "1"
            }
        }    

@relationship(
    name="lab_tests_performed",
    dependencies="lab_tests_performed",
    modifies=[
        "lab_eosino",
        "lab_monocyte",
        "lab_basophil",
        "lab_hemo",
        "lab_bilirubin",
        "lab_pt",
        "lab_inr",
        "lab_aptt",
        "lab_il6",
        "lab_complement",
        "lab_a1c",
        "lab_ph",
        "lab_pco2",
        "lab_pa02",
        "lab_calcium",
        "lab_csf",
        "lab_rbc",
        "lab_csf_protein",
        "lab_csf_glucose",
        "lab_other",
        "lab_other_specify",
        "lab_datetime",
        "abnormal_eosino",
        "abnormal_monocyte",
        "abnormal_basophil",
        "abnormal_hemo",
        "abnormal_bilirubin",
        "abnormal_pt",
        "abnormal_inr",
        "abnormal_aptt",
        "abnormal_il6",
        "abnormal_complement",
        "abnormal_a1c",
        "abnormal_ph",
        "abnormal_pc02",
        "abnormal_pa02",
        "abnormal_calcium",
        "abnormal_csf",
        "abnormal_rbc",
        "abnormal_protein",
        "abnormal_csf_glucose",
        "abnormal_other",
        "abnormal_specify"
    ]
)
# added fillers 
def lab_tests_performed(responses):
    lab_tests_performed = responses["lab_tests_performed"]
    if lab_tests_performed["response_name"] == "1":
        return {
            "lab_eosino": {
                "response_name": "1"
            },
            "lab_monocyte": {
                "response_name": "1"
            },
            "lab_basophil": {
                "response_name": "1"
            },
            "lab_hemo": {
                "response_name": "1"
            },
            "lab_bilirubin": {
                "response_name": "1"
            },
            "lab_pt" : {
                "response_name": "1"
            },
            "lab_inr" : {
                "response_name": "1"
            },
            "lab_aptt": {
                "response_name": "1"
            },
            "lab_il6" : {
                "response_name": "1"
            },
            "lab_complement": {
                "response_name": "1"
            },
            "lab_a1c": {
                "response_name": "1"
            },
            "lab_ph": {
                "response_name": "1"
            },
            "lab_pco2": {
                "response_name": "1"
            },
            "lab_pa02": {
                "response_name": "1"
            },
            "lab_calcium": {
                "response_name": "1"
            },
            "lab_csf" : {
                "response_name": "1"
            },
            "lab_rbc" : {
                "response_name": "1"
            },
            "lab_csf_protein": {
                "response_name": "1"
            },
            "lab_csf_glucose" : {
                "response_name": "1"
            },
            "lab_other": {
                "response_name": "1"
            },
            "lab_other_specify": {
                "response_name": "1"
            },
            "lab_datetime": {
                "response_name": "1"
            },
            "abnormal_eosino": {
                "response_name": "1"
            },
            "abnormal_monocyte": {
                "response_name": "1"
            },
            "abnormal_basophil": {
                "response_name": "1"
            },
            "abnormal_hemo" : {
                "response_name": "1"
            },
            "abnormal_bilirubin" : {
                "response_name": "1"
            },
            "abnormal_pt": {
                "response_name": "1"
            },
            "abnormal_inr" : {
                "response_name": "1"
            },
            "abnormal_aptt": {
                "response_name": "1"
            },
            "abnormal_il6": {
                "response_name": "1"
            },
            "abnormal_complement": {
                "response_name": "1"
            },
            "abnormal_a1c": {
                "response_name": "1"
            },
            "abnormal_ph": {
                "response_name": "1"
            },
            "abnormal_pc02": {
                "response_name": "1"
            },
            "abnormal_pa02" : {
                "response_name": "1"
            },
            "abnormal_calcium" : {
                "response_name": "1"
            },
            "abnormal_csf": {
                "response_name": "1"
            },
            "abnormal_rbc" : {
                "response_name": "1"
            },
            "abnormal_protein": {
                "response_name": "1"
            },
            "abnormal_csf_glucose": {
                "response_name": "1"
            },
            "abnormal_other" : {
                "response_name": "1"
            },
            "abnormal_specify": {
                "response_name": "1"
            }

        }    

@relationship(
    name="viral_positive",
    dependencies= "viral_positive",
    modifies=[
        "viral_testing"
    ]
)
# added fillers 
def viral_positive(responses):
    viral_positive = responses["viral_positive"]
    if viral_positive["response_name"] == "1":
        return {
            "viral_testing": {
                "response_name": "1"
            }
        }    

@relationship(
    name="cardio_assessment",
    dependencies="cardio_assessment",
    modifies=[
        "assessment_date_mdy",
        "abnormality_detail",

    ]
)
# added fillers 
def cardio_assessment(responses):
    cardio_assessment = responses["cardio_assessment"]
    if (cardio_assessment["response_name"] == "1") or (cardio_assessment["response_name"] == "2"):
        return {
            "assessment_date_mdy": {
                "response_name": "1"
            },
            "abnormality_detail": {
                "response_name": "1"
            }
        }    

@relationship(
    name="assessment_other",
    dependencies="assessment_other",
    modifies=[
        "assesment_other_specify"

    ]
)
# added fillers 
def assessment_other(responses):
    assessment_other = responses["assessment_other"]
    if (assessment_other["response_name"] == "1") or (assessment_other["response_name"] == "2"):
        return {
            "assesment_other_specify": {
                "response_name": "1"
            }
        }    

@relationship(
    name="pulm_othertest",
    dependencies="pulm_othertest",
    modifies=[
        "pulmonary_testing_date_mdy",
        "pulm_other_detail"

    ]
)
# added fillers 
def pulm_othertest(responses):
    pulm_othertest = responses["pulm_othertest"]
    if (pulm_othertest["response_name"] == "1") or (pulm_othertest["response_name"] == "2"):
        return {
            "pulmonary_testing_date_mdy": {
                "response_name": "1"
            },
             "pulm_other_detail": {
                "response_name": "1"
            }
        }    

@relationship(
    name="imaging_other",
    dependencies="imaging_other",
    modifies=[
        "imaging_other_detail"

    ]
)
# added fillers 
def imaging_other(responses):
    imaging_other = responses["imaging_other"]
    if (imaging_other["response_name"] == "1") or (imaging_other["response_name"] == "2"):
        return {
            "imaging_other_detail": {
                "response_name": "1"
            }
        }    

@relationship(
    name="ct_brain",
    dependencies="ct_brain",
    modifies=[
        "ct_brain_date_mdy"

    ]
)
# added fillers 
def ct_brain(responses):
    ct_brain = responses["ct_brain"]
    if (ct_brain["response_name"] == "1") or (ct_brain["response_name"] == "2"):
        return {
            "ct_brain_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="ct_chest",
    dependencies="ct_chest",
    modifies=[
        "ct_chest_date_mdy"

    ]
)
# added fillers 
def ct_chest(responses):
    ct_chest = responses["ct_chest"]
    if (ct_chest["response_name"] == "1") or (ct_chest["response_name"] == "2"):
        return {
            "ct_chest_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="ct_abdomen",
    dependencies="ct_abdomen",
    modifies=[
        "ct_ab_date_mdy"

    ]
)
# added fillers 
def ct_abdomen(responses):
    ct_abdomen = responses["ct_abdomen"]
    if (ct_abdomen["response_name"] == "1") or (ct_abdomen["response_name"] == "2"):
        return {
            "ct_ab_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="lung_ultrasound",
    dependencies="lung_ultrasound",
    modifies=[
        "lung_ultrasound_date_mdy"

    ]
)
# added fillers 
def lung_ultrasound(responses):
    lung_ultrasound = responses["lung_ultrasound"]
    if (lung_ultrasound["response_name"] == "1") or (lung_ultrasound["response_name"] == "2"):
        return {
            "lung_ultrasound_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="vasc_ultrasound",
    dependencies="vasc_ultrasound",
    modifies=[
        "vasc_ultrasound_date_mdy"

    ]
)
# added fillers 
def vasc_ultrasound(responses):
    vasc_ultrasound = responses["vasc_ultrasound"]
    if (vasc_ultrasound["response_name"] == "1") or (vasc_ultrasound["response_name"] == "2"):
        return {
            "vasc_ultrasound_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="ab_ultrasound",
    dependencies="ab_ultrasound",
    modifies=[
        "ab_ultrasound_date_mdy"

    ]
)
# added fillers 
def ab_ultrasound(responses):
    ab_ultrasound = responses["ab_ultrasound"]
    if (ab_ultrasound["response_name"] == "1") or (ab_ultrasound["response_name"] == "2"):
        return {
            "ab_ultrasound_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="neonatal_ultrasound",
    dependencies="neonatal_ultrasound",
    modifies=[
        "neonatal_ultrasound_date_mdy"

    ]
)
# added fillers 
def neonatal_ultrasound(responses):
    neonatal_ultrasound = responses["neonatal_ultrasound"]
    if (neonatal_ultrasound["response_name"] == "1") or (neonatal_ultrasound["response_name"] == "2"):
        return {
            "neonatal_ultrasound_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="mri_brain",
    dependencies="mri_brain",
    modifies=[
        "mri_brain_date_mdy"

    ]
)
# added fillers 
def mri_brain(responses):
    mri_brain = responses["mri_brain"]
    if (mri_brain["response_name"] == "1") or (mri_brain["response_name"] == "2"):
        return {
            "mri_brain_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="mri_spine",
    dependencies="mri_spine",
    modifies=[
        "mri_spine_date_mdy"

    ]
)
# added fillers 
def mri_spine(responses):
    mri_spine = responses["mri_spine"]
    if (mri_spine["response_name"] == "1") or (mri_spine["response_name"] == "2"):
        return {
            "mri_spine_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="mri_abdomen",
    dependencies="mri_abdomen",
    modifies=[
        "mri_ab_date_mdy"

    ]
)
# added fillers 
def mri_abdomen(responses):
    mri_abdomen = responses["mri_abdomen"]
    if (mri_abdomen["response_name"] == "1") or (mri_abdomen["response_name"] == "2"):
        return {
            "mri_ab_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="imaging_other",
    dependencies="imaging_other",
    modifies=[
        "mri_other_date_mdy"

    ]
)
# added fillers 
def imaging_other(responses):
    imaging_other = responses["imaging_other"]
    if (imaging_other["response_name"] == "1") or (imaging_other["response_name"] == "2"):
        return {
            "mri_other_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="medications_antibiotics",
    dependencies="medications_antibiotics",
    modifies=[
        "antibiotic_specify"

    ]
)
# added fillers 
def medications_antibiotics(responses):
    medications_antibiotics = responses["medications_antibiotics"]
    if medications_antibiotics["response_name"] == "1":
        return {
            "antibiotic_specify": {
                "response_name": "1"
            }
        }    

@relationship(
    name="medications_diabetic",
    dependencies="medications_diabetic",
    modifies=[
        "medications_insulin"

    ]
)
# added fillers 
def medications_diabetic(responses):
    medications_diabetic = responses["medications_diabetic"]
    if medications_diabetic["response_name"] == "1":
        return {
            "medications_insulin": {
                "response_name": "1"
            }
        }    


@relationship(
    name="medications_other",
    dependencies="medications_other",
    modifies=[
        "medications_other_specify"

    ]
)
# added fillers 
def medications_other(responses):
    medications_other = responses["medications_other"]
    if medications_other["response_name"] == "1":
        return {
            "medications_other_specify": {
                "response_name": "1"
            }
        }    

@relationship(
    name="patient_death",
    dependencies="patient_death",
    modifies=[
        "patient_date_date_mdy"

    ]
)
# added fillers 
def patient_death(responses):
    patient_death = responses["patient_death"]
    if patient_death["response_name"] == "1":
        return {
            "patient_date_date_mdy": {
                "response_name": "1"
            }
        }    

@relationship(
    name="discharge_location",
    dependencies="discharge_location",
    modifies=[
        "discharge_location_other"

    ]
)
# added fillers 
def discharge_location(responses):
    discharge_location = responses["discharge_location"]
    if discharge_location["response_name"] == "1":
        return {
            "discharge_location_other": {
                "response_name": "1"
            }
        }    

@relationship(
    name="treatment_other",
    dependencies="treatment_other",
    modifies=[
        "treatment_other_specify"

    ]
)
# added fillers 
def treatment_other(responses):
    treatment_other = responses["treatment_other"]
    if treatment_other["response_name"] == "1":
        return {
            "treatment_other_specify": {
                "response_name": "1"
            }
        }    
        
@relationship(
    name="treatment_ongoing",
    dependencies="treatment_ongoing",
    modifies=[
        "treatment_stopdt_mdy"
    ]
)
# added fillers 
def treatment_ongoing(responses):
    treatment_ongoing = responses["treatment_ongoing"]
    if treatment_ongoing["response_name"] == "1":
        return {
            "treatment_stopdt_mdy": {
                "response_name": "1"
            }
        }    
        
@relationship(
    name="breakfast_precovid",
    dependencies="breakfast_precovid",
    modifies=[
        "breakfast_duringcovid"
    ]
)
# added fillers 
def breakfast_precovid(responses):
    breakfast_precovid = responses["breakfast_precovid"]
    if breakfast_precovid["response_name"] == "1":
        return {
            "breakfast_duringcovid": {
                "response_name": "1"
            }
        }    

@relationship(
    name="child_iep",
    dependencies="child_iep",
    modifies=[
        "child_iep_precovid",
        "child_iep_duringcovid"
    ]
)
# added fillers 
def child_iep(responses):
    child_iep = responses["child_iep"]
    if child_iep["response_name"] == "2":
        return {
            "child_iep_precovid": {
                "response_name": "1"
            },
            "child_iep_duringcovid": {
                "response_name": "1"
            }
        }    

@relationship(
    name="schooling_middle",
    dependencies="schooling_middle",
    modifies=[
        "schooling_middle_specify"
    ]
)
# added fillers 
def schooling_middle(responses):
    schooling_middle = responses["schooling_middle"]
    if schooling_middle["response_name"] == "6":
        return {
            "schooling_middle_specify": {
                "response_name": "1"
            }
        }    

@relationship(
    name="schooling_present",
    dependencies="schooling_present",
    modifies=[
        "schooling_present_specify"
    ]
)
# added fillers 
def schooling_present(responses):
    schooling_present = responses["schooling_present"]
    if schooling_present["response_name"] == "6":
        return {
            "schooling_present_specify": {
                "response_name": "1"
            }
        }    

@relationship(
    name="hi_loss_covid",
    dependencies="hi_loss_covid",
    modifies=[
        "insur_detail"
    ]
)
# added fillers 
def hi_loss_covid(responses):
    hi_loss_covid = responses["hi_loss_covid"]
    if hi_loss_covid["response_name"] == "1":
        return {
            "insur_detail": {
                "response_name": "1"
            }
        }    

@relationship(
    name="hc_notrec",
    dependencies="hc_notrec",
    modifies=[
        "hc_notrec_detail"
    ]
)
# added fillers 
def hc_notrec(responses):
    hc_notrec = responses["hc_notrec"]
    if hc_notrec["response_name"] == "1":
        return {
            "hc_notrec_detail": {
                "response_name": "1"
            }
        }    

@relationship(
    name="special_ser",
    dependencies="special_ser",
    modifies=[
        "special_ser_during",
        "special_ser_after"
    ]
)
# added fillers 
def special_ser(responses):
    special_ser = responses["special_ser"]
    if special_ser["response_name"] == "1":
        return {
            "special_ser_during": {
                "response_name": "1"
            },
            "special_ser_after": {
                "response_name": "1"
            }
        }    

@relationship(
    name="use_meds",
    dependencies="use_meds",
    modifies=[
        "any_med_condition"
    ]
)
# added fillers 
def use_meds(responses):
    use_meds = responses["use_meds"]
    if use_meds["response_name"] == "1":
        return {
            "any_med_condition": {
                "response_name": "1"
            }
        }    

@relationship(
    name="any_med_condition",
    dependencies="any_med_condition",
    modifies=[
        "any_med_condition_yr"
    ]
)
# added fillers 
def any_med_condition(responses):
    any_med_condition = responses["any_med_condition"]
    if any_med_condition["response_name"] == "1":
        return {
            "any_med_condition_yr": {
                "response_name": "1"
            }
        }    

@relationship(
    name="more_care",
    dependencies="more_care",
    modifies=[
        "any_care_condition"
    ]
)
# added fillers 
def more_care(responses):
    more_care = responses["more_care"]
    if more_care["response_name"] == "1":
        return {
            "any_care_condition": {
                "response_name": "1"
            }
        }    

@relationship(
    name="any_care_condition",
    dependencies="any_care_condition",
    modifies=[
        "any_care_condition_yr"
    ]
)
# added fillers 
def any_care_condition(responses):
    any_care_condition = responses["any_care_condition"]
    if any_care_condition["response_name"] == "1":
        return {
            "any_care_condition_yr": {
                "response_name": "1"
            }
        }    

@relationship(
    name="lim_abil",
    dependencies="lim_abil",
    modifies=[
        "lim_abil_condition"
    ]
)
# added fillers 
def lim_abil(responses):
    lim_abil = responses["lim_abil"]
    if lim_abil["response_name"] == "1":
        return {
            "lim_abil_condition": {
                "response_name": "1"
            }
        }    

@relationship(
    name="lim_abil_condition",
    dependencies="lim_abil_condition",
    modifies=[
        "lim_abil_condition_yr"
    ]
)
# added fillers 
def lim_abil_condition(responses):
    lim_abil_condition = responses["lim_abil_condition"]
    if lim_abil_condition["response_name"] == "1":
        return {
            "lim_abil_condition_yr": {
                "response_name": "1"
            }
        }    

@relationship(
    name="therapy",
    dependencies="therapy",
    modifies=[
        "therapy_condition"
    ]
)
# added fillers 
def therapy(responses):
    therapy = responses["therapy"]
    if therapy["response_name"] == "1":
        return {
            "therapy_condition": {
                "response_name": "1"
            }
        }    

@relationship(
    name="therapy_condition",
    dependencies="therapy_condition",
    modifies=[
        "therapy_condition_yr"
    ]
)
# added fillers 
def therapy_condition(responses):
    therapy_condition = responses["therapy_condition"]
    if therapy_condition["response_name"] == "1":
        return {
            "therapy_condition_yr": {
                "response_name": "1"
            }
        }    

@relationship(
    name="treatment",
    dependencies="treatment",
    modifies=[
        "treatment_yr"
    ]
)
# added fillers 
def treatment(responses):
    treatment = responses["treatment"]
    if treatment["response_name"] == "1":
        return {
            "treatment_yr": {
                "response_name": "1"
            }
        }    

@relationship(
    name="doc_question_yr",
    dependencies="doc_question_yr",
    modifies=[
        "doc_question_yr_detail"
    ]
)
# added fillers 
def doc_question_yr(responses):
    doc_question_yr = responses["doc_question_yr"]
    if doc_question_yr["response_name"] == "1":
        return {
            "doc_question_yr_detail": {
                "response_name": "1"
            }
        }    