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
        df = pd.read_csv('/Users/asiyahahmad/Documents/GitHub/radx-synthetic-cdes/drugsdata.csv')
    
        #Generate a random number between 0 and 15
        num_drugs = random.randint(0, 15)
        
        #Chose the random drug without duplicates in group
        chosen_drugs = []
        drug_classes = set()
        for i in range(num_drugs):
            while True:
                rand_num = random.randint(0, 100000)/100000
                
                #find where the number lies along the cumulative percentage
                #didnt work bc what if the random number was for no row in the cumulative percentage
                # drug_row = df[df['Cumulative Percentage'] >= rand_num].iloc[0]

                #going to change this 
                filtered_rows = df[df['Cumulative Percentage'] >= rand_num]
                if not filtered_rows.empty:
                    drug_row = filtered_rows.iloc[0]
                    #use the drug and note the drug class
                    drug_name = drug_row['Medicine']
                    drug_class = drug_row['Drug Class']
                    
                    #make sure drug class doesnt match any previous ones, append to chosen drug if not
                    if drug_class not in drug_classes:
                        drug_classes.add(drug_class)
                        chosen_drugs.append((drug_name, drug_class))
                        break
                    modified_responses = {}

                    for i, (drug_name, _) in enumerate(chosen_drugs):
                        response_key = f"name_of_rx_med{i+1}"
                        if response_key in responses:
                            modified_responses[response_key] = {
                                "response_name": drug_name
                            }
                    #works
                    return modified_responses
        
   

# @relationship(
#     name="no_chronic_kidney_disease",
#     dependencies=[
#         "nih_chronic_kidney_disease"
#     ],
#     modifies=[
#         "nih_chronic_kidney_disease_treatment"
#     ]
# )
# def no_chronic_kidney_disease(responses):
#     nih_chronic_kidney_disease = responses["nih_chronic_kidney_disease"]
#     if nih_chronic_kidney_disease["response_name"] == "No":
#         return {
#             "nih_chronic_kidney_disease_treatment": {
#                 "response_name": "Skip Logic"
#             }
#         }

# @relationship(
#     name="age_associated_diseases",
#     dependencies=[
#         "nih_age"
#     ],
#     modifies=[
#         "nih_alz",
#         "nih_osteoporosis"
#     ]
# )
# def age_associated_diseases(responses, config):
#     nih_age = responses["nih_age"]
#     if nih_age["response_name"] != "text":
#         return
#     age = int(nih_age["response_value"])
#     """
#     Lerped estimate of the percentage chance that an individual of a given age has an age-progressive disease.

#     :param age: The current age of the individual.
#     :param min_age: The minimum age at which the onset of the disease becomes viable. Before this age, the chance of having the disease is considered 0.
#     :param max_age: The age at which the chance of the onset of a disease caps out. Beyond this age, the chance remains at the cap.
#     :param min_chance: The starting chance of having a disease (for minimized age).
#     :param max_chance: The ending chance of having a disease (as age maxes out).
#     """
#     def disease_chance(age, min_viable_age, max_viable_age, min_chance, max_chance):
#         # Starts at a min_chance % chance of disease
#         # Caps out at a max_chance % chance of disease
#         # min_viable_age: age at which the onset of an age-progressive disease is possible.
#         # max_viable_age: age at which the chance of the onset of an age-progressive disease caps out.
#         age_prop = (age - min_viable_age) / (max_viable_age - min_viable_age)
#         if age_prop < 0: return 0
#         if age_prop > 1: age_prop = 1
#         return lerp(min_chance, max_chance, age_prop)
    
#     ret_val = {}

#     # Begin rolling for diseases
#     if random() < disease_chance(age, **config["nih_alz"]):
#         ret_val["nih_alz"] = {
#             "response_name": "Yes"
#         }
#     if random() < disease_chance(age, **config["nih_osteoporosis"]):
#         ret_val["nih_osteoporosis"] = {
#             "response_name": "Yes"
#         }
#     return ret_val

# @relationship(
#     name="neurodegenerative",
#     dependencies=[
#         "nih_alz"
#     ],
#     modifies=[
#         "nih_neurodegenerative"
#     ]
# )
# def neurodegenerative(responses):
#     nih_alz = responses["nih_alz"]

#     if nih_alz["response_name"] == "Yes":
#         return {
#             "nih_neurodegenerative": {
#                 "response_name": "Yes"
#             }
#         }

# @relationship(
#     name="age_health_status",
#     dependencies=[
#         "nih_age"
#     ],
#     modifies=[
#         "nih_health_status"
#     ]
# )
# def age_health_status(responses, binning_config):
#     nih_age = responses["nih_age"]
#     if nih_age["response_name"] != "text":
#         return
    
#     age = int(nih_age["response_value"])

    
#     excellent = 0
#     very_good = 0
#     good = 0
#     fair = 0
#     poor = 0

#     for bin in binning_config:
#         start_age = bin["start"]
#         end_age = bin["end"]
#         freq_data = bin["data"]
#         if age >= start_age and age <= end_age:
#             excellent += freq_data["excellent"]
#             very_good += freq_data["very_good"]
#             good += freq_data["good"]
#             fair += freq_data["fair"]
#             poor += freq_data["poor"]
    
#     response_name = choices([
#             "Excellent",
#             "Very Good",
#             "Good",
#             "Fair",
#             "Poor"
#         ],
#         weights=[
#             excellent,
#             very_good,
#             good,
#             fair,
#             poor
#         ],
#         k=1
#     )[0]

#     return {
#         "nih_health_status": {
#             "response_name": response_name
#         }
#     }

# @relationship(
#     name="bmi_sleep_apnea",
#     dependencies=[
#         "nih_weight",
#         "nih_height"
#     ],
#     modifies=[
#         "nih_sleep_apnea"
#     ]
# )
# def bmi_sleep_apnea(responses, slope, b, min_freq, max_freq):
#     nih_weight = responses["nih_weight"]
#     nih_height = responses["nih_height"]
    
#     if nih_weight["response_name"] != "integer" or nih_height["response_name"] != "integer":
#         return

#     weight_lb = int(nih_weight["response_value"])
#     height_in = int(nih_height["response_value"])

#     lb_kg_conversion_factor = 0.45359237
#     in_m_conversion_factor = 0.0254

#     # Weight in kilograms
#     weight_kg = weight_lb * lb_kg_conversion_factor
#     # Height in meters
#     height_m = height_in * in_m_conversion_factor

#     bmi = weight_kg / (height_m ** 2)

#     chance = max(min_freq, min(max_freq, slope*bmi + b))
    
    
#     if random() < chance:
#         return {
#             "nih_sleep_apnea": {
#                 "response_name": "Yes"
#             }
#         }

# @relationship(
#     name="heart_attack_angina_cholesterol",
#     dependencies=[
#         "nih_heart_attack"
#     ],
#     modifies=[
#         "nih_cholesterol",
#         "nih_coronary_artery_disease_angina"
#     ]
# )
# def heart_attack_angina_cholesterol(responses, risk_multiplier=1.5):
#     nih_heart_attack = responses["nih_heart_attack"]

#     cholesterol_freq = 0.07
#     angina_freq = 0.01
    
#     if nih_heart_attack["response_name"] == "Yes":
#         # Those who have experienced heart attacks recently will have a 1.5x likelihood of having high cholesterol or angina
#         # Technically, this is actually significantly higher because if the chance isn't rolled here then the user also has to roll against the base chance.
#         # This will be fixed once relationships are transitioned to frequency modifiers rather than response modifiers.
#         cholesterol_freq *= risk_multiplier
#         angina_freq *= risk_multiplier

#         responses = {}
#         if random() < cholesterol_freq:
#             responses["nih_cholesterol"] = {
#                 "response_name": "Yes"
#             }
#         if random() < angina_freq:
#             responses["nih_coronary_artery_disease_angina"] = {
#                 "response_name": "Yes"
#             }
        
#         if len(responses) > 0: return responses


# @relationship(
#     name="pregnancy_prerequisites",
#     dependencies=[
#         "nih_sex",
#         "nih_age"
#     ],
#     modifies=[
#         "nih_pregnancy"
#     ]
# )
# def pregnancy_prerequisites(responses, maximum_viable_age=60):
#     nih_sex = responses["nih_sex"]
#     nih_age = responses["nih_age"]
#     age = int(nih_age["response_value"])

#     if nih_sex["response_name"] != "Female" or age > maximum_viable_age:
#         # Ideally disable `Pregnant` response for non-female/too old.
#         return {
#             "nih_pregnancy": {
#                 "response_name": "Not Pregnant"
#             }
#         }

# @relationship(
#     name="gestational_diabetes",
#     dependencies=[
#         "nih_pregnancy"
#     ],
#     modifies=[
#         "nih_gestational_diabetes"
#     ]
# )
# def gestational_diabetes(responses):
#     nih_pregnancy = responses["nih_pregnancy"]
#     if nih_pregnancy["response_name"] != "Pregnant":
#         return {
#             "nih_gestational_diabetes": {
#                 "response_name": "Skip Logic"
#             }
#         }

# @relationship(
#     name="diabetes_types",
#     dependencies=[
#         "nih_t1d"
#     ],
#     modifies=[
#         "nih_t2dm"
#     ]
# )
# def diabetes_types(responses):
#     nih_t1d = responses["nih_t1d"]
#     if nih_t1d["response_name"] == "Yes":
#         return {
#             "nih_t2dm": {
#                 "response_name": "Skip Logic"
#             }
#         }
# @relationship(
#     name="age_height_association",
#     dependencies=[
#         "nih_sex",
#         "nih_age"
#     ],
#     modifies=[
#         "nih_height"
#     ]
# )
# def age_height(responses, binning_config):
#     nih_sex = responses["nih_sex"]["response_name"]
#     nih_age = responses["nih_age"]

#     if nih_sex != "Male" and nih_sex != "Female":
#         # nih_sex = choices(["Male", "Female"], k=1, weights=[.5, .5])[0]
#         return
#     if nih_age["response_name"] != "text":
#         return

#     age = int(nih_age["response_value"])

#     if nih_sex == "Male":
#         data = binning_config["male"]
#     if nih_sex == "Female":
#         data = binning_config["female"]
    
#     for bin in data:
#         start_age = bin["start"]
#         end_age = bin["end"]
#         freq_data = bin["data"]
#         if age >= start_age and age <= end_age:
#             break

#     bin_data = bin["data"]
#     heights = list(bin_data.keys())
#     weights = list(bin_data.values())
#     height_choice = choices(heights, weights=weights, k=1)[0]
#     return {
#         "nih_height": {
#             "response_name": "integer",
#             "response_value": height_choice
#         }
#     }
    