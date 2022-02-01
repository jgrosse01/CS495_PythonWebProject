"""
Author: Jake Grosse
Date Created: 31 January 2022
Description: A helper file that reads a csv into a dictionary for lookup.
"""


# takes file path from root of this project
def read_csv(file_path="data/MontanaCounties.csv"):
    # boolean flag to exclude the "layout" line of the CSV
    first_line = True
    # init dictionary
    plate_dict = {}
    # open file at selected location
    file = open(f"{file_path}")
    # read lines
    lines = file.readlines()
    # iterate through lines
    for line in lines:
        if not first_line:
            # set the line to the list that contains each comma-delimited item
            line = line.split(',')
            # set dictionary value at the key of plate prefix to the list of county and seat
            plate_dict[int(line[2])] = line[0:2]

        # set flag to False if it was True because the first line has passed
        if first_line:
            first_line = False
    # return the dictionary created
    return plate_dict
