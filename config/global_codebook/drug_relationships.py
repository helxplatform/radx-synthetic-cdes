import random
import pandas as pd
from relationships.register import relationship

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
def take_presc_meds(responses):


    take_presc_meds = responses["take_presc_meds"]

    if take_presc_meds["response_name"] == "No":
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


                take_presc_meds = responses["take_presc_meds"]

                if take_presc_meds["response_name"] == "No":
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
                else:
                    #Set the drug names to the appropriate response keys to return the names of the drug
                    modified_responses = {}
                    for i, (drug_name, _) in enumerate(chosen_drugs):
                        response_key = f"name_of_rx_med{i+1}"
                        if response_key in responses:
                            modified_responses[response_key] = {
                                "response_name": drug_name
                            }
                    #works
                    print("modified" + modified_responses)
                    return modified_responses
                

            else:
                drug_row = None  # Set drug_row to null or any other desired value
                # Rest of your code for handling the case when no rows satisfy the condition


            
           
      


