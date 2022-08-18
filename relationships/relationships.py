from random import random, choice, choices, randint
from .register import relationship

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

@relationship(
    name="no_disability",
    dependencies=[
        "nih_disability"
    ],
    modifies=[
            "nih_deaf",
            "nih_blind",
            "nih_memory",
            "nih_walk_climb",
            "nih_dress_bathe",
            "nih_errand",
    ]
)
def no_disability(responses):
    nih_disability = responses["nih_disability"]
    if nih_disability["response_name"] == "No":
        return {
            "nih_deaf": {
                "response_name": "Skip Logic"
            },
            "nih_blind": {
                "response_name": "Skip Logic"
            },
            "nih_memory": {
                "response_name": "Skip Logic"
            },
            "nih_walk_climb": {
                "response_name": "Skip Logic"
            },
            "nih_dress_bathe": {
                "response_name": "Skip Logic"
            },
            "nih_errand": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="no_smoking",
    dependencies=[
        "nih_smoking_yn"
    ],
    modifies=[
        "nih_vaping_yn",
        "nih_nicotine_yn",
        "nih_vape_freq",
        "nih_cig_smoke_freq"
    ]
)
def no_smoking(responses):
    nih_smoking_yn = responses["nih_smoking_yn"]
    if nih_smoking_yn["response_name"] == "No":
        return {
            "nih_vaping_yn": {
                "response_name": "Skip Logic"
            },
            "nih_nicotine_yn": {
                "response_name": "Skip Logic"
            },
            "nih_vape_freq": {
                "response_name": "Skip Logic"
            },
            "nih_cig_smoke_freq": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="no_alcohol",
    dependencies=[
        "nih_alcohol_yn"
    ],
    modifies=[
        "nih_lifetime_use_alcohol",
        "nih_alcohol_yrs",
        "nih_alcohol_frequency"
    ]
)
def no_alcohol(responses):
    nih_alcohol_yn = responses["nih_alcohol_yn"]
    if nih_alcohol_yn["response_name"] == "No":
        return {
            "nih_lifetime_use_alcohol": {
                "response_name": "Skip Logic"
            },
            "nih_alcohol_yrs": {
                "response_name": "Skip Logic"
            },
            "nih_alcohol_frequency": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="no_cancer",
    dependencies=[
        "nih_cancer"
    ],
    modifies=[
        "nih_cancer_active_treatment",
        "nih_cancer_past_yr"
    ]
)
def no_cancer(responses):
    nih_cancer = responses["nih_cancer"]
    if nih_cancer["response_name"] == "No":
        return {
            "nih_cancer_active_treatment": {
                "response_name": "Skip Logic"
            },
            "nih_cancer_past_yr": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="no_chronic_kidney_disease",
    dependencies=[
        "nih_chronic_kidney_disease"
    ],
    modifies=[
        "nih_chronic_kidney_disease_treatment"
    ]
)
def no_chronic_kidney_disease(responses):
    nih_chronic_kidney_disease = responses["nih_chronic_kidney_disease"]
    if nih_chronic_kidney_disease["response_name"] == "No":
        return {
            "nih_chronic_kidney_disease_treatment": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="age_associated_diseases",
    dependencies=[
        "nih_age"
    ],
    modifies=[
        "nih_alz",
        "nih_neurodegenerative",
        "nih_osteoporosis"
    ]
)
def age_associated_diseases(responses):
    nih_age = responses["nih_age"]
    age = int(nih_age["response_value"])
    def lerp(a, b, t):
        return a + t * (b - a)
    """
    Lerped estimate of the percentage chance that an individual of a given age has an age-progressive disease.

    :param age: The current age of the individual.
    :param min_age: The minimum age at which the onset of the disease becomes viable. Before this age, the chance of having the disease is considered 0.
    :param max_age: The age at which the chance of the onset of a disease caps out. Beyond this age, the chance remains at the cap.
    :param min_chance: The starting chance of having a disease (for minimized age).
    :param max_chance: The ending chance of having a disease (as age maxes out).
    """
    def disease_chance(age, min_age=50, max_age=80, min_chance=0.005, max_chance=0.05):
        # # Starts at a 0.5% chance of disease
        # min_chance = 0.005
        # # Caps out at a 5% chance of disease
        # max_chance = 0.05
        # # Age at which the onset of an age-progressive disease is possible.
        # min_age = 50
        # # Age at which the chance of the onset of an age-progressive disease caps out.
        # max_age = 88

        age_prop = (age - min_age) / (max_age - min_age)
        if age_prop < 0: return 0
        if age_prop > 1: age_prop = 1
        return lerp(min_chance, max_chance, age_prop)
    
    ret_val = {}

    # Begin rolling for diseases
    if random() < disease_chance(age):
        ret_val["nih_alz"] = {
            "response_name": "Yes"
        }
    if random() < disease_chance(age):
        ret_val["nih_neurodegenerative"] = {
            "response_name": "Yes"
        }
    if random() < disease_chance(
        age,
        min_age=40
    ):
        ret_val["nih_osteoporosis"] = {
            "response_name": "Yes"
        }
    return ret_val

@relationship(
    name="age_health_status",
    dependencies=[
        "nih_age"
    ],
    modifies=[
        "nih_health_status"
    ]
)
def age_health_status(responses):
    nih_age = responses["nih_age"]
    age = int(nih_age["response_value"])

    excellent = 0.1
    very_good = 0.2
    good = 0.2
    fair = 0.2
    poor = 0.2
    dont_know = 0.05
    prefer_not_to_answer = 0.05

    if 0 <= age and age <= 10:
        excellent += 0.05
        very_good += 0.05
        good += 0.15

        fair -= 0.10
        poor -= 0.15
    elif 11 <= age and age <= 20:
        excellent += 0.05
        very_good += 0.05
        good += 0.10

        fair -= 0.075
        poor -= 0.125
    elif 21 <= age and age <= 40:
        very_good += 0.05
        good += 0.025

        fair -= 0.025
        poor -= 0.05
    elif 41 <= age and age <= 60:
        excellent -= 0.05
        very_good -= 0.15
        good -= 0.10
        
        fair += 0.20
        poor += 0.10
    elif 61 <= age and age <= 80:
        excellent -= 0.075
        very_good -= 0.125
        good -= 0.125

        fair += 0.125
        poor += 0.20
    elif 81 <= age:
        excellent -= 0.09
        very_good -= 0.15
        good -= 0.15

        fair += 0.14
        poor += 0.25
    
    response_name = choices([
            "excellent",
            "very_good",
            "good",
            "fair",
            "poor",
            "dont_know",
            "prefer_not_to_answer"
        ],
        weights=[
            excellent,
            very_good,
            good,
            fair,
            poor,
            dont_know,
            prefer_not_to_answer
        ],
        k=1
    )[0]

    return {
        "nih_health_status": {
            "response_name": response_name
        }
    }

@relationship(
    name="weight_sleep_apnea",
    dependencies=[
        "nih_weight"
    ],
    modifies=[
        "nih_sleep_apnea"
    ]
)
def weight_sleep_apnea(responses):
    nih_weight = responses["nih_weight"]["response_value"]

    weight_min, weight_max = (40, 300)

    weight_norm = (nih_weight - weight_min) / (weight_max - weight_min)
    sleep_apnea_freq = 0.15

    # Quadratic curve where the bottom percentiles are skewed somewhat against sleep apnea (0.5x as likely (half as likely))
    # and upper percentiles are skewed strongly against sleep apnea (2.5x more likely)
    relative_risk = (weight_norm + 0.5) ** 2 + 0.25
    chance = sleep_apnea_freq * relative_risk
    
    if random() < chance:
        return {
            "nih_sleep_apnea": {
                "response_name": "Yes"
            }
        }

@relationship(
    name="heart_attack_angina_cholesterol",
    dependencies=[
        "nih_heart_attack"
    ],
    modifies=[
        "nih_cholesterol",
        "nih_coronary_artery_disease_angina"
    ]
)
def heart_attack_angina_cholesterol(responses):
    nih_heart_attack = responses["nih_heart_attack"]

    cholesterol_freq = 0.07
    angina_freq = 0.01
    
    if nih_heart_attack["response_name"] == "Yes":
        # Those who have experienced heart attacks recently will have a 1.5x likelihood of having high cholesterol or angina
        # Technically, this is actually significantly higher because if the chance isn't rolled here then the user also has to roll against the base chance.
        # This will be fixed once relationships are transitioned to frequency modifiers rather than response modifiers.
        cholesterol_freq *= 1.5
        angina_freq *= 1.5

        responses = {}
        if random() < cholesterol_freq:
            responses["nih_cholesterol"] = {
                "response_name": "Yes"
            }
        if random() < angina_freq:
            responses["nih_coronary_artery_disease_angina"] = {
                "response_name": "Yes"
            }
        
        if len(responses) > 0: return responses


@relationship(
    name="pregnancy_prerequisites",
    dependencies=[
        "nih_sex",
        "nih_age"
    ],
    modifies=[
        "nih_pregnancy"
    ]
)
def pregnancy_prerequisites(responses):
    nih_sex = responses["nih_sex"]
    nih_age = responses["nih_age"]
    age = int(nih_age["response_value"])

    if nih_sex["response_name"] != "Female" or age > 60:
        # Ideally disable `Pregnant` response for non-female/too old.
        return {
            "nih_pregnancy": {
                "response_name": "Not Pregnant"
            }
        }

@relationship(
    name="gestational_diabetes",
    dependencies=[
        "nih_pregnancy"
    ],
    modifies=[
        "nih_gestational_diabetes"
    ]
)
def gestational_diabetes(responses):
    nih_pregnancy = responses["nih_pregnancy"]
    if nih_pregnancy["response_name"] != "Pregnant":
        return {
            "nih_gestational_diabetes": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="diabetes_types",
    dependencies=[
        "nih_t1d"
    ],
    modifies=[
        "nih_t2dm"
    ]
)
def diabetes_types(responses):
    nih_t1d = responses["nih_t1d"]
    if nih_t1d["response_name"] == "Yes":
        return {
            "nih_t2dm": {
                "response_name": "Skip Logic"
            }
        }

@relationship(
    name="covid_symptom_clustering",
    dependencies=[],
    modifies=[
        "nih_skin_rash",
        "nih_conjunctivitis",
        "nih_red_eyes",
        "nih_high_temp",
        "nih_no_sympt",
        "nih_blue_lips",
        "nih_balance",
        "nih_slurred_peech",
        "nih_neuro_shakes",
        "nih_numb_extremities",
        "nih_sweating",
        "nih_seizures",
        "nih_rash_toes",
        "nih_cough",
        "nih_fever_chills",
        "nih_diff_breath",
        "nih_headache",
        "nih_muscle_ache",
        "nih_olfactory",
        "nih_fatigue",
        "nih_nausea_vomiting_diarrhea",
        "nih_abdom_pain",
        "nih_throat_congestion_nose",
        "nih_other_symp",
        "nih_wheezing",
        "nih_confusion",
        "nih_appetite"
    ]
)
def covid_symptom_clustering(responses, clusters_config):
    covid_freq = clusters_config["covid_freq"]
    global_symptoms = clusters_config["global_symptoms"]
    clusters = clusters_config["cluster_symptoms"]
    for cluster in clusters:
        cluster["symptoms"] = {
            **global_symptoms,
            **cluster["symptoms"]
        }
    if random() >= covid_freq: return

