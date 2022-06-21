from .register import relationship
from random import random

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
                "response_name": "No"
            },
            "nih_nicotine_yn": {
                "response_name": "No"
            },
            "nih_vape_freq": {
                "response_name": "Not at all"
            },
            "nih_cig_smoke_freq": {
                "response_name": "Not at all"
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
                "response_name": "No"
            },
            "nih_alcohol_yrs": {
                "response_name": "Never"
            },
            "nih_alcohol_frequency": {
                "response_name": "Never"
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
                "response_name": "No"
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