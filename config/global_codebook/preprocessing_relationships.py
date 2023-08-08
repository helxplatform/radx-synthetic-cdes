from random import random, choice, choices, randint
from relationships.register import relationship

@relationship(
    name="covid_symptom_clustering",
    dependencies=None,
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
    
    cluster = choices(
        clusters,
        weights=[cluster["frequency"] for cluster in clusters],
        k=1
    )[0]
    
    modified_responses = {}
    for variable in cluster["symptoms"]:
        responses = cluster["symptoms"][variable]
        used_freq = sum(responses.values())
        no_change_freq = 1 - used_freq

        response_name = choices(
            [
                *responses.keys(),
                None
            ],
            weights=[
                *responses.values(),
                no_change_freq
            ],
            k=1
        )[0]
        if response_name is not None:
            modified_responses[variable] = {
                "response_name": response_name
            }
    
    return modified_responses