# Przemyslaw Bil
# g00398317@atu.ie
# Multi Paradigm Programming 2022

# Shop simulation written using Procedural Python

import csv
import os
from ShopFunctions import display_menu, get_user_selection, get_user_number, defineMenuChoices
from ShopErrors import BudgetTooLowError, NotEnoughStockError

def create_and_stock_shop(path):

    # define a shop as a dictionary
    shop={
        "cash": 0, 
        "products":[]
        }

    with open(path) as stock_file:
        csv_reader = csv.reader(stock_file, delimiter=',')

        first_row = next(csv_reader)
        shop["cash"]=float(first_row[0])

        #shop["products"] = []

        for row in csv_reader:

            product={}

            product["name"] = row[0]
            product["price"] = float(row[1])
            product["qty"] = int(row[2])

            shop["products"].append(product)

    return shop

def read_customer(csv_path):


    with open(csv_path) as stock_file:

        csv_reader = csv.reader(stock_file, delimiter=',')

        first_row = next(csv_reader)

        # define the customer dictionary
        customer={
            "name" : first_row[0],
            "cash": float(first_row[1]),
            "payment_due": 0,
            "shopping_list": []
        }

        for row in csv_reader:

            product={
                "name" : row[0],
                "qty" : int(row[1]),
                "price": 0,
                "basket_qty": 0,
                "bag_qty": 0
            }

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

    print("\n{} wants to buy: ".format(cust["name"]))

    print("Shopping list:")
    for product in cust["shopping_list"]:

        print("NAME: {},  PRICE: €{:.2f}, REQUIRED QUANTITY: {:3d}, IN THE BASKET: {:3d}".format(product["name"], product["price"], product["qty"], product["basket_qty"]))

    rest = cust["cash"] - customer["payment_due"]
    print("------------------------------------------")
    print("The total cost would be: €{:.2f}, he would have €{:.2f} left".format(customer["payment_due"], rest))

# method to save all exceptions to csv file
def addToExceptionsFiles(ef_path, msg):

    # as per https://www.pythontutorial.net/python-basics/python-write-csv-file/ and 
    # https://stackoverflow.com/questions/13203868/how-to-write-to-csv-and-not-overwrite-past-text 
    with open(ef_path, 'a', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        # as per https://stackoverflow.com/questions/1816880/why-does-csvwriter-writerow-put-a-comma-after-each-character
        writer.writerow([msg])   


# function to look for items from the customre shopping list in the shops stock,
# putting found items to the shopping basket and calculating the total cost
def fill_shopping_basket(customer, shop, ef_path):

    # keep tally of the total cost of all the products in the shoppibg list
    payment_due = 0

    # Loop over the customers shopping list
    for list_item in customer["shopping_list"]:
        # loop over the products in the shops stock
        for stock_item in shop["products"]:

            # If product from shopping list is found in the shops stock, put it in the basket
            if list_item["name"] == stock_item["name"]:
                
                # make sure shop has enough stock to fulfill the order
                if stock_item["qty"] >= list_item["qty"]:
                    qty = list_item["qty"]                    
                else:
                # if it doesn't, put in the basket whatever is left in stock
                    qty = stock_item["qty"]
                    err_msg = "There is not enough {} in stock. Actual stock: {}, required Stock {} ".format(list_item["name"] , qty, list_item["qty"])
                    addToExceptionsFiles(ef_path, err_msg)
                
                # Remove required qty from the shops stock
                stock_item["qty"]-=qty

                # put the required amount of selected product into the shopping basket
                list_item["basket_qty"] = qty                

                list_item["price"] = stock_item["price"]

                # calculate full amount due for all the available items
                payment_due += qty*stock_item["price"]
    
    # assign the payment_due in customer dict with sum of the values of items in the shopping basket
    customer["payment_due"] = payment_due

    return customer, shop



def finilize_transaction(customer, shop, ef_path):

    # try to pay for every basket item individually
    for basket_item in customer["shopping_list"]:

        while basket_item['basket_qty']>0:

            payment_due =  basket_item['basket_qty']*basket_item['price']
            # Check if the customer has enough money to pay for the item in the basket
            if customer['cash'] >= payment_due:

                # Pay for the items
                customer['cash'] -= payment_due
                shop['cash'] += payment_due
                # Empty the basket into the bag
                basket_item['bag_qty'] = basket_item['basket_qty']
                basket_item['basket_qty'] = 0
                
                # stop the while loop
                # break
            # If the customer doesn't have enough money to pay for all the items, remove one item from the basket                
            else:
                # Add error message to the Exceptions file
                err_msg = "{} has not enough money to pay for {} units of {} worth {:.2f} as he/she has only {:.2f}".format(
                                customer['name'], 
                                basket_item['basket_qty'], 
                                basket_item['name'], 
                                basket_item['basket_qty']*basket_item['price'], 
                                customer['cash']  
                            )
                addToExceptionsFiles(ef_path, err_msg)                                
                # remove one item from the basket and check again if the customer can afford it
                basket_item['basket_qty']-=1
                # find the product in the shop and return one item from the basket back to the shop
                for product in shop['products']:
                    if product['name'] == basket_item['name']:
                        product['qty'] += 1
                        break
    
    # return changed customer and shop variables
    return customer, shop

# main for function call
if __name__ == "__main__":

    # File path for the shop's csv file
    shop_csv_path = 'stock.csv'
    # File path for customer's csv file
    customer_csv_path = 'customer.csv'
    # File path for the Exceptions csv file
    exceptions_csv_path ='Exceptions.csv'

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

            # Read the customre shopping list from the file
            customer = read_customer(customer_csv_path)

            # fill customers basket based on the shopping list and available stock in shop
            customer, myShop = fill_shopping_basket(customer, myShop, exceptions_csv_path)

            print("\nShop and the Customer pre-transaction:\n")
            print_shop(myShop)
            print_customer(customer)            

            # Pause to give user chance to read Customer and Shop states before the transaction
            input("Press ENTER to finilize the sale")

            finilize_transaction(customer, myShop, exceptions_csv_path)

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

        

        

    

        