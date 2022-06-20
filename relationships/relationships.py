from .register import relationship

@relationship(
    name="no_disability",
    dependencies={
        "nih_disability": ["No"]
    },
    modifies={
            "nih_deaf": "Skip Logic",
            "nih_blind": "Skip Logic",
            "nih_memory": "Skip Logic"
    }
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
            }
        }