from random import random, randint, choice, choices
from relationships.register import udf

"""
UDFs are currently ran once during generation, and that is the only time.
Therefore, this rudimentary solution should be alright to use. Not great,
but it gets the job done rather than adding further complexity to configuration.
"""
class UniqueRecordGenerator:
    def __init__(self):
        self.available_record_ids = None
        self.min = None
        self.max = None
    def configure(self, min, max):
        if self.min != min or self.max != max:
        # Range upper argument is exclusive
            self.available_record_ids = list(range(min, max + 1))
        self.min = min
        self.max = max
    def generate(self):
        if len(self.available_record_ids) == 0:
            raise Exception("Ran out of record ids. You are may be trying to generate more records than the amount of possible record_ids.")
        id = choice(self.available_record_ids)
        self.available_record_ids.remove(id)
        return id
record_generator = UniqueRecordGenerator()
@udf("test_record_id")
def test_record_id(upper_id=999999):
    """ Return a string in the format "TEST_######" where "######" represents a random 6 digit, 0-padded number. """
    record_generator.configure(0, upper_id)
    id = record_generator.generate()
    x = str(id).rjust(6, "0")
    return f"TEST_{x}"

@udf("age_generator")
def age_generator(binning_config):
    # Choose a bin based on frequency fields
    bin = choices(binning_config, weights=[bin["frequency"] for bin in binning_config], k=1)[0]
    start = bin["start"]
    end = bin["end"]
    return str(randint(start, end))
            

@udf("zip_code_generator")
def zip_code_generator():
    # Valid US postal codes range from 00001-99999.
    return str(randint(1, 99999)).rjust(5, "0")
    
@udf("weight_distribution")
def weight_distribution():
    ...
    
@udf("height_distribution")
def height_distribution():
    ...