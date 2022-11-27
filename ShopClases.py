import csv

# Define the Custom Error Classes
# from https://www.programiz.com/python-programming/user-defined-exception
class NotEnoughStockError(Exception):
    pass

class BudgetTooLowError(Exception):
    pass

# defining the Product class
# This class will describe a product in the shop
class Product:
    
    # Constructor function
    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
    # print function
    def __repr__(self):
        return "NAME: {}, PRICE: €{:.2f} ".format(self.name, self.price)

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

        # Decrese the Shop stock by the qty from the shopping list
        # If not enough in stock, set stock to 0
        # Return the actual sale quantity
        if  self.quantity >= askedSalesQty:      
            self.quantity -= askedSalesQty
        else:            
            self.quantity = 0
            raise NotEnoughStockError("Not enough stock!")
        
        # Return the actual sales quantity
        return oldQty-self.quantity


    def setQty(self, newQty):
        self.quantity = newQty

    # print function: Returns the Name of the product and it's stock level        
    def __repr__(self):
        return "{} STOCK QUANTITY: {:3d}".format(self.product, self.quantity)


class ShoppingListItem(ProductStock):

        # Constructor function (takes objects of Product class and quantity)
    def __init__(self, product, quantity):

        super().__init__(product, quantity)
        self.afterTransaction = False
    
    #def isAfterTransaction(self):
     #   return self.afterTransaction

    def __repr__(self):
        if self.afterTransaction:
            return "{} BOUGHT QUANTITY: {:3d}".format(self.product, self.quantity)
        else:
            return "{} REQUIRED QUANTITY: {:3d}".format(self.product, self.quantity)           

    # Override parent class setQty method. This method will be used to set the bought qty (after transaction)
    def setQty(self, newQty):
        super().setQty(newQty)
        self.afterTransaction = True       

# Define the Customer class
class Customer:

    # Constructor function
    # needs customer name and the budget
    def __init__(self, path="", name="", budget=0):

        # Use this variable to store if the transaction has been completed
        self.transactionCompleted = False

        # Shopping list: list of Products to buy
        self.shopping_list = []

        if len(path)==0:
            self.name = name
            self.budget = budget
        else:
            # Read the customer infor from the specified csv file
            with open(path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                # Read first row of scv file and use it to specified to shopping budget of the customer
                first_row = next(csv_reader)
                self.name = first_row[0]
                self.budget = float(first_row[1])

                # Read the 2nd line the shopping items
                for row in csv_reader:
                    name = row[0]
                    quantity = int(row[1])
                    # Use 'name' to initialize an instance of a Product class
                    p = Product(name)
                    # Use the the instance of Product class and required quantity to initialize and instance of ShoppingListItem class                
                    self.shopping_list.append(ShoppingListItem(p, quantity)) 

    
    # Add product to the shopping list (shopping cart)
    def addItemToShoppingCart(self, productName, prodQty, prodCost):

        p = Product(productName, prodCost)
        self.shopping_list.append(ShoppingListItem(p, prodQty))


    # function to calculate the total cost of the customers order
    def getOrder_cost(self):
        cost = 0
        
        # loop over the shopping list and sum the costs of each items
        for list_item in self.shopping_list:
            cost += list_item.getCost()
        
        return cost

    def getName(self):
        return self.name

    def getShoppingList(self):
        return self.shopping_list

    def setTransactionCompleted(self):
        self.transactionCompleted = True

    def isTransactionCompleted(self):
        return self.transactionCompleted

    # Method to finilize the transaction
    # If the funds are sufficient, Customer budget is decreased by the cost of the items 
    # If the budget is too low, BudgetTooLowError is raised
    def payForItem(self, shoppingListItem):

        prePayBudget = self.budget

        if self.budget >= shoppingListItem.getCost():
            self.budget -= shoppingListItem.getCost()

        else:
            raise BudgetTooLowError

        return prePayBudget - self.budget       
    
    def __repr__(self):
        
        if self.isTransactionCompleted():
            str =  "{} bought:".format(self.name) 
        else:
            str =  "{} wants to buy:".format(self.name) 

        # Loop over the Shopping list and print a total cost of each items
        for item in self.shopping_list:
            cost = item.getCost()
            str += "\n{} ".format(item)

            # if cost of the Shopping list item is 0, print this message:
            if (item.getUnitPrice() == 0):
                str +=  "{} doesn't know how much that costs :(".format(self.name)
            else:
            # otherwise, print the cost of the item
                str += " COST: €{:.2f}".format(cost)

        # add a message describing money left from the Customre budget after the shopping             
        str +="\n------------------------------------------"
        str += "\nThe total cost would be: €{:.2f}, he would have €{:.2f} left\n".format(self.getOrder_cost(), self.budget)
        return str 


# Define the Shop Class
class Shop:
    
    # Constructor function, path to the csv file with the Shops stock must be specified
    def __init__(self, shop_path, exception_path):
        self.stock = []

        # Store the path of theexception file
        self.exceptionsFilePath = exception_path

        # open the csv file with the Shops stock
        with open(shop_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, int(row[2]))
                self.addToStock(ps)
    
    def __repr__(self):
        str = ""
        str += "Shop has €{:.2f} in cash\n".format(self.cash)
        for item in self.getStock():
            str += "{}\n".format(item)
        return str

    # Define function to add stock item to Shops stock
    def addToStock(self, stock_item):
        self.stock.append(stock_item)

    # Define function to retrieve Shops stock items
    def getStock(self):
        return self.stock

    def addToExceptionsFiles(self, msg):

        # TODO: add msg to file Exceptions.csv

        print(msg)

    # Method to search Shops stock by the product name
    # If product is found, Unit price and stock Qty is returned
    # If no product of that name is found, 0,0 is returned
    def checkStockByName(self, searched_name):

        for stock_item in self.stock:
            if stock_item.getName()==searched_name:
                return stock_item
        
        # If above loop doesn't find the searched product
        # Return instance of the ProductStock object with cost of 0 and 0 stock
        return ProductStock(Product(searched_name, 0), 0)

    # Define function to perform the sales transaction
    def performSales(self, customer):

        # Sum cost of all items to clalculate the total transaction cost
        transactionCost = 0

        # loop over the customers shopping list (array of ShoppingListItem Class Objects)
        for shopping_list_item in customer.getShoppingList():
            # find the matching product in the Shops stock (array of ProductStock Class Objects)
            for stock_item in self.stock:            
                # check if product name on the shopping list matches name in the stock
                if (shopping_list_item.getName() == stock_item.getName()):

                    # if it matches, get its price and assign it to the price of the items on ths shopping list
                    shopping_list_item.getProduct().setPrice(stock_item.getUnitPrice())

                    initialStock = stock_item.getQty()

                    # Get the required product qty form the shopping list
                    askedSalesQty = shopping_list_item.getQty()

                    # Decrese the Shop stock by the qty from the shopping list
                    # If not enough in stock, set stock to 0
                    # Return the actual sale quantity
                    try:
                        actualSalesQty = stock_item.changeQty(askedSalesQty)
                    except NotEnoughStockError:
                        actualSalesQty = initialStock
                        self.addToExceptionsFiles("There is not enough {} in stock. Actual stock: {}, required Stock {} ".format(shopping_list_item.getName(), actualSalesQty, askedSalesQty))

                    # Set the shopping list to the actual sales quantity
                    shopping_list_item.setQty(actualSalesQty)         

                                        
                    # If customer have enough money, pay for the items
                    try:
                        self.cash += customer.payForItem(shopping_list_item)
                    except BudgetTooLowError:
                        self.addToExceptionsFiles("{} has not enough money to pay for {} {} worth €{:.2f} as he has only €{:.2f} \n".format(
                            customer.getName(), actualSalesQty, shopping_list_item.getName(), shopping_list_item.getCost(), customer.budget ))

                        # Roll back on customer and shop stock changes
                        shopping_list_item.setQty(0)
                        stock_item.setQty(initialStock)                            
                        
        customer.setTransactionCompleted()

        return transactionCost