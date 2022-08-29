from random import random
from relationships.register import relationship

@relationship(
    name="insomnia_vaping",
    dependencies=[
        "nih_vape_freq"
    ],
    modifies=[
        "nih_insomnia"
    ]
)
def insomnia_vaping(responses, config):
    nih_vape_freq = responses["nih_vape_freq"]

    insomnia_freq = 0.02

    if nih_vape_freq["response_name"] == "Rarely":
        insomnia_freq *= config["rarely"]
    elif nih_vape_freq["response_name"] == "Some Days":
        insomnia_freq *= config["some_days"]
    elif nih_vape_freq["response_name"] == "Every Day":
        insomnia_freq *= config["every_day"]
    
    if random() < insomnia_freq:
        return {
            "nih_insomnia": "Yes"
        }