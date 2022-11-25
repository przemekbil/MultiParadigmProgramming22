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

# defining the ProductStock class
# This class will keep track of the stock levels for each product in the shop and on the customers shopping list
class ProductStock:
    
    # Constructor function (takes objects of Product class and quantity)
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    # defining function to get the name of the product
    def getName(self):
        return self.product.name;
    
    # defining function to get the Unit price of the product
    def getUnitPrice(self):
        return self.product.price;

    #defining function to get the total cost of of all the products in stock  
    def getCost(self):
        return self.getUnitPrice() * self.quantity

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
        str += "\nThe cost would be: €{:.2f}, he would have €{:.2f} left".format(self.getOrder_cost(), self.budget - self.getOrder_cost())
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

# Create an instance of the Shop class
s = Shop("stock.csv")
print(s)

# Create an instance of the Customer class
c = Customer("customer.csv")
c.calculate_costs(s.getStock())
print(c)