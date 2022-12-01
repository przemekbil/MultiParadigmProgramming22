# Przemyslaw Bil
# g00398317@atu.ie
# Multi Paradigm Programming 2022

# Collections of Python functions used by both Shop programs: written using Object Oriented and Procedural paradigms

import csv
import datetime

# Re-used from 3rd semester Algorithms module
# Inspired by https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/
def display_menu(options, level=0, title="MAIN MENU"):

    # add empty line before and after the menu
    print()
    print(title)
    # print the Menu options on the screen

    # Add extra spaces depending on the level of the Menu
    prefix = ""
    for i in range(level):
        prefix += "   "

    for key in options:
        print("{}{}---{}".format(prefix, key, options[key]))
    print()

# Re-used from 3rd semester Algorithms module
# Function to read user menu selection
# msg - message to be displayed to prompt user for input
# err_msg - error message to display when input other than number is sleected
def get_user_selection(msg, err_msg):

    # Infinite loop
    while True:
        # Try to convert input into integer
        # if it's not possible, display error message and wait for user input
        try:
            choice = int(input(msg))
            break
        except:
            print(err_msg)

    # Return the number selected by the user
    return choice

# Function to read user menu selection
# msg - message to be displayed to prompt user for input
# err_msg - error message to display when input other than number is sleected
def get_user_number(msg, err_msg):

    # Infinite loop
    while True:
        # Try to convert input into integer
        # if it's not possible, display error message and wait for user input
        try:
            choice = float(input(msg))
            break
        except:
            print(err_msg)

    # Return the number selected by the user
    return choice

# Function returns the menu options for both the Manin Menu and the live shop menu
def defineMenuChoices():
    
    # selection options for the main menu
    main = {
        1: 'Read Shopping list from file',
        2: 'Live mode',
        0: 'Exit'
    }

    # Selection options for the live shop menu
    live = {
        3: 'Ask for product',
        4: 'Check the shopping cart',
        5: 'Pay for items',
        0: 'Exit'
    }

    return main, live

# method to save all exceptions to csv file
def addToExceptionsFiles(ef_path, msg):

    # as per https://www.pythontutorial.net/python-basics/python-write-csv-file/ and 
    # https://stackoverflow.com/questions/13203868/how-to-write-to-csv-and-not-overwrite-past-text 
    with open(ef_path, 'a', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f, delimiter=",")
        # Add a space at the beggining of the error message and remove the " character
        msg = ' ' + msg
        # as per https://stackoverflow.com/questions/1816880/why-does-csvwriter-writerow-put-a-comma-after-each-character        
        writer.writerow([datetime.datetime.now(), msg])