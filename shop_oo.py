import ShopClases

# Re-used from 3rd semester Algorithms module
# Inspired by https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/
def main_menu():

    # define the options for the menu to be displayed for the user
    options={
        1: 'Read Shopping list from file',
        2: 'Live mode',
        0: 'Exit'
    }

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


def read_shopping_list_from_file(myShop):

    # Create an instance of the Customer class by reading the shopping list from the file
    customer1 = ShopClases.Customer("customer.csv")

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

    print("Live mode shop")

# main for function call
if __name__ == "__main__":

    # Create an instance of the Shop class
    myShop = ShopClases.Shop("stock.csv", "Exceptions.csv")

    # initialize user_choice=1, to allow for the while loop below to run
    user_choice = 1

    # display the user Menu until 0 is selected
    while user_choice!=0:   

        # Display Menu 
        main_menu()
        # Get users choice
        user_choice = get_user_input('Enter your choice: ', '\nPlease input a number')        

        # Choice 1: Read shopping list from file
        if user_choice == 1:
            read_shopping_list_from_file(myShop)
            input("Press enter to continue...")

        elif user_choice == 2:
            live_mode(myShop)
            input("Press enter to continue...")          

        elif user_choice==0:
            print("Exiting")
        
        else:
            # if number other than 0, 1, 2, display this message
            print("\n{} is not a vlid option menu!\n".format(user_choice))            