import ShopClases

# main for function call
if __name__ == "__main__":

    # Create instance of both Customer and Shop classes
    # Create an instance of the Shop class
    myShop = ShopClases.Shop("stock.csv", "Exceptions.csv")
    # Create an instance of the Customer class
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