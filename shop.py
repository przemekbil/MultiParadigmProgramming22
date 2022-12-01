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

    # variable to count all the products in the basket
    baset_qty = 0

    # variable to count the cost of purchased items
    payed = 0

    print("\n{} has €{:.2f} in cash. ".format(cust["name"], cust["cash"]))
    print("Shopping list:")
    for product in cust["shopping_list"]:

        print("NAME: {},  PRICE: €{:.2f}, REQUIRED QUANTITY: {:3d}, IN THE BASKET: {:3d}, IN THE BAG: {:3d}".format(
            product["name"], 
            product["price"], 
            product["qty"], 
            product["basket_qty"],
            product["bag_qty"]
            )
        )

        # Sum up all the products in the basket
        baset_qty += product["basket_qty"]

        # calculat ethe total cost of items purchased
        payed += product["bag_qty"]*product["price"]

    # print the mesage
    print("------------------------------------------")
    if baset_qty> 0:
        rest = cust["cash"] - cust["payment_due"]
        print("The total cost would be: €{:.2f}, he would have €{:.2f} left\n".format(cust["payment_due"], rest))
    else:
        print("The total cost of purchased items: €{:.2f}. There is €{:.2f} left\n".format(payed, cust["cash"]))

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


    # Loop over the customers shopping list. Filter shopping list for products that have basket_qty==0
    # Filter as per https://stackoverflow.com/questions/29051573/python-filter-list-of-dictionaries-based-on-key-value
    # The filtering is done to loop only over new products (products not in the basket yet)
    for list_item in list(filter(lambda d: d['basket_qty'] in [0], customer["shopping_list"])):
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

                # Assign the price 
                list_item["price"] = stock_item["price"]

    # keep tally of the total cost of all the products in the shopping list
    payment_due = 0

    # Sum all the products in the baskets
    for basket_item in customer["shopping_list"]:
        # calculate full amount due for all the available items
        payment_due += basket_item["basket_qty"] *basket_item["price"]
    
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


def live_shop_mode(shop, live_menu, ef_path):

    os.system('cls')
    print("Live mode shop")

    customer_name = input("Please enter the Customer name: ")
    customer_budget = get_user_number('Please enter the Customer budget: ', '\nPlease input a number')

    liveCustomer = {
        "name" : customer_name,
        "cash": customer_budget,
        "payment_due": 0,
        "shopping_list": []
    }

    while True:
        # Clear the console
        os.system('cls')
        # Display Menu       
        display_menu(live_menu, 1, "LIVE SHOP MENU")
        # Get users choice
        user_choice = get_user_selection('Enter your choice: ', '\nPlease input a number')

        if user_choice == 3:
            # Ask the user for th eproduct name
            prod_name = input("Please enter the product name: ")

            available_qty = 0
            unit_price = 0

            # Check if product is found in Shops stock
            for product in shop["products"]:

                if product["name"]  == prod_name:
                    available_qty = product["qty"]
                    unit_price = product["price"]
                    break

            
            if available_qty== 0:
                print("The Shop doesn't have {} in stock".format(prod_name))
            else:
                print("The Shop has {} units of {} in stock. The unit price is €{}\n".format(available_qty, prod_name, unit_price ))
                req_amount = get_user_selection("Please specified the required amount: ", "'\nPlease input a whole number'")

                # Keep asking the user for the new amount until it's equal or smaller than the stock
                # Selecting 0 will cancel the order
                #while req_amount > available_qty:
                #    req_amount = get_user_selection("The shop doesn't have sufficient stock to fulfill this order. Please enter amount less or equal to {} or 0 to cancel: ".format(available_qty),
                #     "'\nPlease input a whole number'")

                if req_amount > 0:
                    product={
                        "name" : prod_name,
                        "qty" : req_amount,
                        "price": unit_price,
                        "basket_qty": 0,
                        "bag_qty": 0
                    }

                    liveCustomer["shopping_list"].append(product)
                    
                    # Check the shop's stock and put products in the shopping basket
                    fill_shopping_basket(liveCustomer, shop, ef_path)

            
            # Ask the Shop for the prices and stock level of required product
            # shopStockItem = myShop.checkStockByName(prod_name)
        elif user_choice == 4:
            # Clear the console
            os.system('cls')            
            print_shop(shop)
            print_customer(liveCustomer)
            input("\nPress ENTER to continue")

        elif  user_choice == 5:
            # Clear the console
            os.system('cls')

            # Finilize the transaction
            finilize_transaction(liveCustomer, shop, exceptions_csv_path)

            # Print the shop and customer states after the transaction
            print("\nShop and the Customer post-transaction:\n")
            print_shop(shop)
            print_customer(liveCustomer) 

            input("Press enter to continue...")                           


        elif user_choice == 0:
            print("Exiting to Main Menu")
            break
        else:
            print("\n{} is not a vlid option menu!\n".format(user_choice))             


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

            # Clear the console
            os.system('cls')            

            # Read the customre shopping list from the file
            customer = read_customer(customer_csv_path)

            # fill customers basket based on the shopping list and available stock in shop
            customer, myShop = fill_shopping_basket(customer, myShop, exceptions_csv_path)

            print("\nShop and the Customer pre-transaction:\n")
            print_shop(myShop)
            print_customer(customer)            

            # Pause to give user chance to read Customer and Shop states before the transaction
            input("Press ENTER to finilize the sale")
            # Clear the console
            os.system('cls')

            finilize_transaction(customer, myShop, exceptions_csv_path)

            print("\nShop and the Customer post-transaction:\n")
            print_shop(myShop)
            print_customer(customer) 

            input("Press enter to continue...")

        # Choice 1: Read shopping list from file
        if user_choice == 2:
            live_shop_mode(myShop, live_menu, exceptions_csv_path)
        
        # Choice 0: Exit the program
        elif user_choice==0:
            print("Exiting")
            break
        
        # Any other choice: display error message
        else:
            # if number other than 0, 1, 2, display this message
            print("\n{} is not a vlid option menu!\n".format(user_choice))    

        

        

    

        