# Przemyslaw Bil
# g00398317@atu.ie
# Multi Paradigm Programming 2022

# Shop simulation written using Procedural Python

import csv
import os
from ShopFunctions import display_menu, get_user_selection, get_user_number, defineMenuChoices
from ShopErrors import BudgetTooLowError

def create_and_stock_shop(path):

    shop={}

    with open(path) as stock_file:
        csv_reader = csv.reader(stock_file, delimiter=',')

        first_row = next(csv_reader)
        shop["cash"]=float(first_row[0])

        shop["products"] = []

        for row in csv_reader:

            product={}

            product["name"] = row[0]
            product["price"] = float(row[1])
            product["qty"] = int(row[2])

            shop["products"].append(product)

    return shop

def read_customer(csv_path):

    customer={}

    with open(csv_path) as stock_file:

        csv_reader = csv.reader(stock_file, delimiter=',')

        first_row = next(csv_reader)

        customer["name"]=first_row[0]
        customer["cash"]=float(first_row[1])

        customer["shopping_list"] = []

        for row in csv_reader:

            product={}

            product["name"] = row[0]
            product["qty"] = int(row[1])

            customer["shopping_list"].append(product)

    return customer    


# Function to print the informatiopn about the product in stock/shopping list
def print_product(p):
    print("NAME: {}, PRICE: €{:.2f}, STOCK QUANTITY: {:3d}".format(p["name"], p["price"], p["qty"]))
    pass

def print_shop(s):
    print("Shop has €{:.2f} in cash".format(s["cash"]))
    print("Stock:")
    for product in s["products"]:
        print_product(product)


def print_customer(cust):

    # keep tally of the total cost of all the products in the shoppibg list
    total_cost = 0

    print("\n{} wants to buy: ".format(cust["name"]))
    #print("Name: {}, Cash: {}".format(cust["name"], cust["cash"]))

    print("Shopping list:")
    for product in cust["shopping_list"]:
        print("NAME: {},  REQUIRED QUANTIT: {}".format(product["name"], product["qty"]))

    rest = cust["cash"] - total_cost
    print("------------------------------------------")
    print("The total cost would be: €{:.2f}, he would have €{:.2f} left".format(total_cost, rest))   



# main for function call
if __name__ == "__main__":

    # File path for the shop's csv file
    shop_csv_path = 'stock.csv'
    # File path for suctomer's csv file
    customer_csv_path = 'customer.csv'    

    # Initialize myShop variable by reading shop status from the csv file
    myShop = create_and_stock_shop(shop_csv_path)

    # define the options for the menu to be displayed for the user
    main_menu, live_menu = defineMenuChoices()


    # display the user Menu until 0 is selected
    while True:   

        # Clear the console
        os.system('cls')
        # Display Menu       
        display_menu(main_menu, 0)
        # Get users choice
        user_choice = get_user_selection('Enter your choice: ', '\nPlease input a number')

        # Choice 1: Read shopping list from file
        if user_choice == 1:            

            customer = read_customer(customer_csv_path)

            print("\nShop and the Customer pre-transaction:\n")
            print_shop(myShop)
            print_customer(customer)
            # Pause to give user chance to read Customer and Shop states before the transaction
            input("Press ENTER to finilize the sale")

            print("\nShop and the Customer post-transaction:\n")

            input("Press enter to continue...")

        # Choice 0: Exit the program
        elif user_choice==0:
            print("Exiting")
            break
        
        # Any other choice: display error message
        else:
            # if number other than 0, 1, 2, display this message
            print("\n{} is not a vlid option menu!\n".format(user_choice))    

        

        

    

        