from .register import relationship
from random import random

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
    def disease_chance():
        # Starts at a 0.5% chance of disease
        min_chance = 0.8
        # Caps out at a 5% chance of disease
        max_chance = 1
        # Age at which the onset of an age-progressive disease is possible
        min_age = 50
        # Age at which the chance of the onset of an age-progressive disease caps out.
        max_age = 88

        age_prop = (age - min_age) / (max_age - min_age)
        if age_prop < 0: return 0
        if age_prop > 1: age_prop = 1
        return lerp(min_chance, max_chance, age_prop)
    

    ret_val = {}

    chance = disease_chance()
    # Begin rolling for diseases
    if random() < chance:
        ret_val["nih_alz"] = {
            "response_name": "Yes"
        }
    if random() < chance:
        ret_val["nih_neurodegenerative"] = {
            "response_name": "Yes"
        }
    if random() < chance:
        ret_val["nih_osteoporosis"] = {
            "response_name": "Yes"
        }
    return ret_val