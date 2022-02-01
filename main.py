"""
Author:         Jake Grosse
Date Created:   31 January 2022
Description:    The main python file for this webapp. It manages routing and gets/posts
                as well as handling backend processing.
"""

# general imports
from flask import Flask, redirect, render_template, request, url_for
from lookup.Reader import read_csv
from lookup.Lookup import lookup
import re


# make it webby
app = Flask(__name__)

# dictionary containing lookup tables
license_dict = {}


# display initial webpage
@app.route("/", methods=["GET"])
def start():
    return render_template("index.html")


# load the general invalid input page
@app.route("/invalid_input", methods=["GET"])
def invalid_input():
    return render_template("invalid_input.html")


# load the string invalid input page
@app.route("/str_invalid_input", methods=["GET"])
def str_invalid_input():
    return render_template("str_invalid_input.html")


# load the empty box invalid input page
@app.route("/no_invalid_input", methods=["GET"])
def no_invalid_input():
    return render_template("no_invalid_input.html")


# display's the dictionary read from the csv file provided as a table in HTML
@app.route("/see_table", methods=["GET"])
def display_table():
    global license_dict

    # string to be returned
    ret_string = ""
    # header string
    ret_string = ret_string + "<h1>Montana County License Plate Prefix Lookup Table</h1><br>"
    # sub-head string
    ret_string = ret_string + "<h2>Sorted Alphabetically by County of Residence</h2>"
    # return link
    ret_string = ret_string + "<a href=\"/\">Return to Search Page</a><br><br>"

    # append initial table row for labels
    ret_string = ret_string + "<table>"
    ret_string = ret_string + "<tr>"
    ret_string = ret_string + "<th style=\"text-align:left;\">License Prefix</th>"
    ret_string = ret_string + "<th style=\"text-align:left;\">County of Residence</th>"
    ret_string = ret_string + "<th style=\"text-align:left;\">Seat City</th>"
    ret_string = ret_string + "</tr>"

    # systematically append dictionary items
    for key in license_dict.keys():
        ret_string = ret_string + "<tr>"
        ret_string = ret_string + f"<td>{key}</td>"
        ret_string = ret_string + f"<td>{license_dict[key][0]}</td>"
        ret_string = ret_string + f"<td>{license_dict[key][1]}</td>"
        ret_string = ret_string + "</tr>"

    # ends table
    ret_string = ret_string + "</table>"

    # return the whole table string
    return ret_string


# redirect to a result page when looking through dictionary
@app.route("/results", methods=["POST"])
def results():
    # get global
    global license_dict

    # initialize flag variables
    wants_county = False
    wants_seat = False

    # get the search key
    key = request.form['prefix']
    # can't figure out regex's so here's a list of characters :)
    char_list = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-',
                 '+', '=', '\\', '[', ']', '{', '}', '"', "'", '<', '>', ':', ';', '/', '.', ',', '|']

    # strip all the characters
    for char in char_list:
        key = key.strip(char)

    try:
        # determine whether a search query wants county or seat or both
        wants_county = request.form['output'] == "county" or request.form['output'] == "county-seat"
        wants_seat = request.form['output'] == "seat" or request.form['output'] == "county-seat"
    except:
        # if they do not select, assume both
        wants_county = True
        wants_seat = True

    # if the user inputs nothing, empty box invalid input
    if key == '':
        return redirect(url_for('no_invalid_input'))

    # make sure it is an integer input, if it is not then except for invalid input type string
    try:
        # if it is castable, it will be an int for easier use after this point
        key = int(key)
    except:
        return redirect(url_for('str_invalid_input'))

    # get lookup result
    lookup_result = lookup(key, license_dict)

    # if there is no entry (handled in lookup method) then generic invalid input page
    if not lookup_result[0]:
        return redirect(url_for('invalid_input'))

    # initialize the string of html to be returned
    ret_string = ""

    # if they want both outputs
    if wants_county and wants_seat:
        # make that string
        ret_string = ret_string + f"<h3>License plate code {key} is tied to {license_dict[key][0]} County with a\
         Seat City of {license_dict[key][1]}.</h3>"

        # just an easter egg
        if key == 42:
            ret_string = ret_string + "<p>Congratulations! You found the meaning of life!</p>"
            ret_string = ret_string + "<p>Have a fantastic A Capella Doo-Wop song from a singer\
                    with amazing range, Tim Foust!</p>"
            ret_string = ret_string + '<iframe width="560" height="315" src="https://www.youtube.com/embed/lnk1_IkqdLA"\
                    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;\
                    encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br>'
    # if they want only seat
    elif wants_seat:
        # make that string
        ret_string = ret_string + f"<h3>License plate code {key} is tied to the Seat\
         City of {license_dict[key][1]}.</h3>"

        # just an easter egg
        if key == 42:
            ret_string = ret_string + "<p>Congratulations! You found the meaning of life!</p>"
            ret_string = ret_string + "<p>Have a fantastic A Capella Doo-Wop song from a singer\
                     with amazing range, Tim Foust!</p>"
            ret_string = ret_string + '<iframe width="560" height="315" src="https://www.youtube.com/embed/lnk1_IkqdLA"\
                    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;\
                    encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br>'
    # if they want only county (only option left)
    else:
        # make that string
        ret_string = ret_string + f"<h3>License plate code {key} is tied to the County of {license_dict[key][0]}.</h3>"

        # just an easter egg
        if key == 42:
            ret_string = ret_string + "<p>Congratulations! You found the meaning of life!</p>"
            ret_string = ret_string + "<p>Have a fantastic A Capella Doo-Wop song from a singer\
                    with amazing range, Tim Foust!</p>"
            ret_string = ret_string + '<iframe width="560" height="315" src="https://www.youtube.com/embed/lnk1_IkqdLA"\
                    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;\
                    encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br>'

    # no matter what, always add the option to return to the search page
    ret_string = ret_string + "<a href=\"/\">Return to Search Page</a>"
    # return the compiled return string
    return ret_string


# main method, literally just reads in CSV and starts the webserver
if __name__ == '__main__':
    # load in dictionary from the CSV file (default argument with path)
    license_dict = read_csv()
    # start app
    app.run(debug=True)
