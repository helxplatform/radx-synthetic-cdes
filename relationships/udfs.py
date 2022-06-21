from random import randint
from .register import udf

@udf("test_record_id")
def test_record_id():
    """ Return a string in the format "TEST_######" where "######" represents a random 6 digit, 0-padded number. """
    x = str(randint(0, 999999)).rjust(6, "0")
    return f"TEST_{x}"

@udf("age_generator")
def age_generator(min_age, max_age):
    """ Return a number in the inclusive range [min_age, max_age]. """
    # In the future, perhaps a probability distribution could be added.
    return randint(min_age, max_age)