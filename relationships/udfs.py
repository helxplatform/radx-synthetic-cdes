from random import randint, choice
from .register import udf

"""
UDFs are currently ran once during generation, and that is the only time.
Therefore, this rudimentary solution be alright to use. Not great, but it gets the job done rather than
adding further complexity to configuration.
"""
used_record_ids = []
@udf("test_record_id")
def test_record_id():
    """ Return a string in the format "TEST_######" where "######" represents a random 6 digit, 0-padded number. """
    # Range upper argument is exclusive, so choices are actually from 0-999999
    num_choices = list(set(range(0, 1000000)).difference(used_record_ids))
    if len(num_choices) == 0:
        raise Exception("Ran out of record ids. You are may be trying to generate more records than the amount of possible record_ids.")
    x = str(choice(num_choices)).rjust(6, "0")
    return f"TEST_{x}"

@udf("age_generator")
def age_generator(min_age, max_age):
    """ Return a number in the inclusive range [min_age, max_age]. """
    # In the future, perhaps a probability distribution could be added.
    return randint(min_age, max_age)

@udf("zip_code_generator")
def zip_code_generator():
    # Valid US postal codes range from 00001-99999.
    return str(randint(1, 99999)).rjust(5, "0")
    