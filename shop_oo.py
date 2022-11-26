import csv

# defining the Product class
# This class will describe a product in the shop
class Product:
    
    # Constructor function
    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
    # print function
    def __repr__(self):
        return "NAME: {}, PRICE: €{} ".format(self.name, self.price)

    # Define a function to return the products name
    def getName(self):
        return self.name

    # define a function to return the products price
    def getPrice(self):
        return self.price

    # define a function to set an item price (used in Customer shopping list)
    def setPrice(self, newPrice):
        self.price = newPrice

# defining the ProductStock class
# This class will keep track of the stock levels for each product in the shop and on the customers shopping list
class ProductStock:
    
    # Constructor function (takes objects of Product class and quantity)
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    # defining function to get the name of the product
    def getName(self):
        return self.product.getName()
    
    # defining function to get the Unit price of the product
    def getUnitPrice(self):
        return self.product.getPrice()

    def getProduct(self):
        return self.product

    #defining function to get the total cost of of all the products in stock  
    def getCost(self):
        return self.getUnitPrice() * self.quantity

    def getQty(self):
        return self.quantity

    # Change incrementally the stock qty by the asked sales Qty
    def changeQty(self, askedSalesQty):

        oldQty = self.quantity

        # check if stock is enough to perform the sales for full qty
        if  self.quantity >= askedSalesQty:      
            self.quantity -= askedSalesQty
        else:
            self.quantity = 0
        
        # Return the actual sales quantity
        return oldQty-self.quantity


    def setQty(self, newQty):
        self.quantity = newQty

    # print function: Returns the Name of the product and it's stock level        
    def __repr__(self):
        return "{} STOCK QUANTITY: {}".format(self.product, self.quantity)   #f"{self.product} QUANTITY: {self.quantity}"


# Define the Customer class
class Customer:

    # Constructor function
    # needs Path of the csv file with customer specification
    def __init__(self, path):

        # Shopping list: list of Products to buy
        self.shopping_list = []

        # Read the customer infor from the csv file
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Read first row of scv file and use it to specified to shopping budget of the customer
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])

            # Read the 2nd line the shopping items
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                # Use 'name' to unitialize an instance of a Product class
                p = Product(name)
                # Use the the instance of Product class and required quantity to initialize and instance of ProductStock class
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps) 

    # function to calculate the todatl cost of the shopping list                
    def calculate_costs(self, shopStock):
        # loop over products in the shops stock
        for shop_item in shopStock:
            # loop over the shopping list
            for list_item in self.shopping_list:
                # check if product name on the shopping list matches name in the stock
                if (list_item.getName() == shop_item.getName()):
                    # if it matches, get its price and assign it to the price of the items on ths shopping list
                    list_item.product.price = shop_item.getUnitPrice()
    
    # function to calculate the total cost of the customers order
    def getOrder_cost(self):
        cost = 0
        
        # loop over the shopping list and sum the costs of each items
        for list_item in self.shopping_list:
            cost += list_item.getCost()
        
        return cost

    def getShoppingList(self):
        return self.shopping_list
    
    def __repr__(self):
        
        str =  "{} wants to buy".format(self.name) #f"{self.name} wants to buy"
        # Loop over the Shopping list and print a total cost of each items
        for item in self.shopping_list:
            cost = item.getCost()
            str += "\n{} ".format(item)

            # if cost of the Shopping list item is 0, print this message:
            if (cost == 0):
                str +=  "{} doesn't know how much that costs :(".format(self.name)
            else:
            # otherwise, print the cost of the item
                str += " COST: €{}".format(cost)

        # add a message describing money left from the Customre budget after the shopping                
        str += "\nThe cost would be: €{:.2f}, he would have €{:.2f} left\n".format(self.getOrder_cost(), self.budget - self.getOrder_cost())
        return str 


# Define the Shop Class
class Shop:
    
    # Constructor function, path to the csv file with the Shops stock must be specified
    def __init__(self, path):
        self.stock = []

        # open the csv file with the Shops stock
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.addToStock(ps)
    
    def __repr__(self):
        str = ""
        str += "Shop has €{} in cash\n".format(self.cash)
        for item in self.getStock():
            str += "{}\n".format(item)
        return str

    # Define function to add stock item to Shops stock
    def addToStock(self, stock_item):
        self.stock.append(stock_item)

    # Define function to retrieve Shops stock items
    def getStock(self):
        return self.stock

    # Define function to perform the sales transaction
    def performSales(self, shoppingList):
        cost = 0

        # loop over products in the shops stock ((array of Stock Class Objects))
        for stock_item in self.stock:
            # loop over the shopping list (array of Stock Class Objects)
            for shopping_list_item in shoppingList:
                # check if product name on the shopping list matches name in the stock
                if (shopping_list_item.getName() == stock_item.getName()):
                    # if it matches, get its price and assign it to the price of the items on ths shopping list
                    shopping_list_item.getProduct().setPrice(stock_item.getUnitPrice())

                    # Get the required product qty form the shopping list
                    askedSalesQty = shopping_list_item.getQty()

                    # Decrese the Shop stock by the qty from the shopping list
                    # If not enough in stock, set stock to 0
                    # Return the actual sale quantity
                    actualSalesQty = stock_item.changeQty(askedSalesQty)

                    # Set the shopping list to the actual sales quantity
                    shopping_list_item.setQty(actualSalesQty)
                    
                    # Calculate the cost using updated Shopping list qty using the actual sales qty
                    cost += shopping_list_item.getCost()

        self.cash += cost

        return cost

# Create an instance of the Shop class
myShop = Shop("stock.csv")

print("\nShop and the Customer pre-transaction: \n")

print(myShop)

# Create an instance of the Customer class
customer1 = Customer("customer.csv")

print(customer1)

customer1.calculate_costs(myShop.getStock())

myShop.performSales(customer1.getShoppingList())

print("Shop and the Customer post-transaction: \n")

print(customer1)

print(myShop)