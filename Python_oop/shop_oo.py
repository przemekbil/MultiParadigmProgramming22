# Przemyslaw Bil
# g00398317@atu.ie
# Multi Paradigm Programming 2022

# Shop simulation written using Object Oriented Python


# Import custom Shop and Customer classes
from ShopClases import Customer, Shop
import os
from ShopErrors import BudgetTooLowError
from ShopFunctions import display_menu, get_user_selection, get_user_number, defineMenuChoices
#import sys

#sys.path.insert(0, '/home/admin/Documents/GMIT/MultiParadigmProgramming22/Python_proc')
    

# Function used to read the Customer's shopping list from the csv file
def read_shopping_list_from_file(sl_path, myShop):

    # Create an instance of the Customer class by reading the shopping list from the file
    customer1 = Customer(sl_path)

    # Print customer and shop states before the transaction
    print("\nShop and the Customer pre-transaction: \n")
    print(myShop)
    print(customer1)

    # Pause to give user chance to read Customer and Shop states before the transaction
    input("Press ENTER to finilize the sale")

    # Perform the sales transaction
    myShop.performSales(customer1)

    # Print the states of both objects after the transaction
    print("Shop and the Customer post-transaction: \n")
    print(customer1)
    print(myShop)

    return customer1


def live_mode(myShop, Live_shop_options, exceptions_csv_path):

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
    print("Live mode shop")

    customer_name = input("Please enter the Customer name: ")
    customer_budget = get_user_number('Please enter the Customer budget: ', '\nPlease input a number')

    liveCustomer = Customer(name=customer_name, budget=customer_budget)


    while True:

        # Display the live shop menu options
        display_menu(Live_shop_options, 1, "LIVE SHOP MENU")
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

                # Add new shopping list item
                liveCustomer.addItemToShoppingList(prod_name, shopStockItem.getUnitPrice(), req_amount)

                # Put available products into the shopping basket
                liveCustomer.fill_shopping_basket(myShop, exceptions_csv_path)

                

        elif user_choice == 4:
            # Clear the console
            os.system('cls' if os.name=='nt' else 'clear')           
            print(myShop)
            print(liveCustomer)
            input("Press ENTER to continue")
        elif user_choice == 5:
             # Perform the sales transaction
            try:
                # Clear the console
                os.system('cls' if os.name=='nt' else 'clear')
                # Perform the sales transaction
                myShop.performSales(liveCustomer, exceptions_csv_path)
                # Print the state of Customer and Shop after the transaction
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
    # File path for the shop's csv file
    shop_csv_path = '../stock.csv'
    # File path for customer's csv file
    customer_csv_path = '../customer.csv'
    # File path for the Exceptions csv file
    exceptions_csv_path ='../Exceptions.csv'    

    # Create an instance of the Shop class
    myShop = Shop(shop_csv_path, exceptions_csv_path)

    # define the options for the menu to be displayed for the user
    main_menu_options, Live_shop_options = defineMenuChoices()

    # display the user Menu until 0 is selected
    while True:   

        # Display Menu       
        display_menu(main_menu_options, 0)
        # Get users choice
        user_choice = get_user_selection('Enter your choice: ', '\nPlease input a number')        

        # Choice 1: Read shopping list from file
        if user_choice == 1:

            # Create an instance of the Customer class by reading the shopping list from the file
            customer = Customer(customer_csv_path)

            # Fill out the customer's basket 
            customer.fill_shopping_basket(myShop, exceptions_csv_path)            

            os.system('cls' if os.name=='nt' else 'clear')
            # Print customer and shop states before the transaction
            print("Shop and the Customer pre-transaction: \n")
            print(myShop)
            print(customer)

            # Pause to give user chance to read Customer and Shop states before the transaction
            input("Press ENTER to finilize the sale")
            os.system('cls' if os.name=='nt' else 'clear')

            # Perform the sales transaction
            myShop.performSales(customer, exceptions_csv_path)

            # Print the states of both objects after the transaction
            print("Shop and the Customer post-transaction: \n")
            print(myShop)              
            print(customer)         

            input("Press enter to continue...")

        elif user_choice == 2:
            live_mode(myShop, Live_shop_options, exceptions_csv_path)
            #input("Press enter to continue...")          

        elif user_choice==0:
            print("Exiting")
            break
        
        else:
            # if number other than 0, 1, 2, display this message
            print("\n{} is not a vlid option menu!\n".format(user_choice))            