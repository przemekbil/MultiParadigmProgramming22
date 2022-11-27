import ShopClases

# Re-used from 3rd semester Algorithms module
# Inspired by https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/
def display_menu(options):

    # add empty line before and after the menu
    print()
    # print the Menu options on the screen
    for key in options:
        print("{}---{}".format(key, options[key]))
    print()

# Re-used from 3rd semester Algorithms module
# Function to read user numerical input
# msg - message to be displayed to prompt user for input
# err_msg - error message to display when input other than number is sleected
def get_user_input(msg, err_msg):

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
        4: 'Check balance',
        0: 'Exit'
    }

    print("Live mode shop")

    while True:

        display_menu(Live_shop_options)
        # Get users choice
        user_choice = get_user_input('Enter your choice: ', '\nPlease input a number')

        if user_choice == 3:
            # Ask the user for th eproduct name
            prod_name = input("Please enter the product name: ")
            
            # Ask the Shop for the prices and stock level of required product
            prod_price, prod_stock = myShop.checkStockByName(prod_name)

            # Check if product is found in Shops stock
            if prod_price == 0:
                print("The Shop doesn't have {} in stock".format(prod_name))
            else:
                print("The Shop has {} units of {} in stock. The unit price is €{} ".format(prod_stock, prod_name, prod_price))
                req_amount = get_user_input("Please specified the required amount: ", "'\nPlease input a whole number'")

                while req_amount > prod_stock:
                    req_amount = get_user_input("The shop doesn't have sufficient stock to filfill this order. Please enter new amount or 0 to exit: ", "'\nPlease input a whole number'")

        elif user_choice == 4:
            print("Check balance: ")
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

        # Display Menu 
        display_menu(main_menu_options)
        # Get users choice
        user_choice = get_user_input('Enter your choice: ', '\nPlease input a number')        

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