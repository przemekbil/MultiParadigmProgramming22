# Przemyslaw Bil
# g00398317@atu.ie
# Multi Paradigm Programming 2022

# Shop simulation written using Object Oriented Python


# Import custom Shop and Customer classes
import ShopClases
import os
from ShopErrors import BudgetTooLowError
from ShopFunctions import display_menu, get_user_selection, get_user_number

    

# Function used to read the Customer's shopping list from the csv file
def read_shopping_list_from_file(sl_path, myShop):

    # Create an instance of the Customer class by reading the shopping list from the file
    customer1 = ShopClases.Customer(sl_path)

    # Print customer and shop states before the transaction
    print("\nShop and the Customer pre-transaction: \n")
    print(myShop)
    print(customer1)

    # Perform the sales transaction
    myShop.performSales(customer1)

    # Print the states of both objects after the transaction
    print("Shop and the Customer post-transaction: \n")
    print(customer1)
    print(myShop)


def live_mode(myShop):

    Live_shop_options = {
        3: 'Ask for product',
        4: 'Check the shopping cart',
        5: 'Pay for items',
        0: 'Exit'
    }

    # Clear the console
    os.system('cls')
    print("Live mode shop")

    customer_name = input("Please enter the Customer name: ")
    customer_budget = get_user_number('Please enter the Customer budget: ', '\nPlease input a number')

    liveCustomer = ShopClases.Customer(name=customer_name, budget=customer_budget)


    while True:
        # Clear the console
        os.system('cls')
        # Display the live shop menu options
        display_menu(Live_shop_options, 1)
        # Get users choice
        user_choice = get_user_selection('Enter your choice: ', '\nPlease input a number')

        if user_choice == 3:
            # Ask the user for th eproduct name
            prod_name = input("Please enter the product name: ")
            
            # Ask the Shop for the prices and stock level of required product
            shopStockItem = myShop.checkStockByName(prod_name)

            # Check if product is found in Shops stock
            if shopStockItem.getQty() == 0:
                print("The Shop doesn't have {} in stock".format(prod_name))
            else:
                print("The Shop has {} units of {} in stock. The unit price is €{} ".format(shopStockItem.getQty(), prod_name, shopStockItem.getUnitPrice()))
                req_amount = get_user_selection("Please specified the required amount: ", "'\nPlease input a whole number'")

                # Keep asking the user for the new amount until it's equal or smaller than the stock
                # Selecting 0 will cancel the order
                while req_amount > shopStockItem.getQty():
                    req_amount = get_user_selection("The shop doesn't have sufficient stock to fulfill this order. Please enter amount less or equal to {} or 0 to cancel: ".format(shopStockItem.getQty()),
                     "'\nPlease input a whole number'")

                liveCustomer.addItemToShoppingCart(prod_name, req_amount, shopStockItem.getUnitPrice())
                #print("You requested for {} units of {} which will cost {}. Do you want to coninue?".format(req_amount, prod_name, shopStockItem.getCost()))

                

        elif user_choice == 4:
            # Clear the console
            os.system('cls')            
            print(myShop)
            print(liveCustomer)
            input("Press ENTER to continue")
        elif user_choice == 5:
             # Perform the sales transaction
            try:
                # Clear the console
                os.system('cls')
                myShop.performSales(liveCustomer)
                print(myShop)
                print(liveCustomer)
                input("Press ENTER to continue")
            except BudgetTooLowError:
                print("\nERROR: The customer has insufficient funds to complete this transaction!\n")
                input("Press ENTER to continue")
            # Print customer and shop states after the transaction
          
        elif user_choice == 0:
            print("Exiting to Main Menu")
            break
        else:
            print("\n{} is not a vlid option menu!\n".format(user_choice)) 

# main for function call
if __name__ == "__main__":

    # Create an instance of the Shop class
    myShop = ShopClases.Shop("stock.csv", "Exceptions.csv")

    # define the options for the menu to be displayed for the user
    main_menu_options = {
        1: 'Read Shopping list from file',
        2: 'Live mode',
        0: 'Exit'
    }

    # display the user Menu until 0 is selected
    while True:   

        # Clear the console
        os.system('cls')
        # Display Menu       
        display_menu(main_menu_options, 0)
        # Get users choice
        user_choice = get_user_selection('Enter your choice: ', '\nPlease input a number')        

        # Choice 1: Read shopping list from file
        if user_choice == 1:
            read_shopping_list_from_file("customer.csv", myShop)
            input("Press enter to continue...")

        elif user_choice == 2:
            live_mode(myShop)
            #input("Press enter to continue...")          

        elif user_choice==0:
            print("Exiting")
            break
        
        else:
            # if number other than 0, 1, 2, display this message
            print("\n{} is not a vlid option menu!\n".format(user_choice))            