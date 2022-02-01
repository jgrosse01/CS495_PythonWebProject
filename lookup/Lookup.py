"""
Author: Jake Grosse
Date Created: 31 January 2022
Description: A helper file used to look up a county and seat city by licence plate key given a dictionary.
"""


# simply looks up and returns the value located at the key along
# with a boolean to check if the value is "NONE"

# this exists to separate the code out into several files
# and keep it neater

# takes key to lookup, dictionary to search, and two booleans for what to return
def lookup(key, dictionary):
    # value directly from dictionary if it doesn't exist then set to none
    try:
        temp_value = dictionary[int(key)]
    except:
        temp_value = None

    # if the value is None, package with False, otherwise package with True
    if temp_value is None:
        # actual value to be returned
        ret_val = [False, temp_value]
    else:
        # actual value to be returned
        ret_val = [True, temp_value]

    # simply return value packaged with whether a value was found
    return ret_val

