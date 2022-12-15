# Przemyslaw Bil
# g00398317@atu.ie
# Multi Paradigm Programming 2022

# Collections of Classes used in shop simulation written using Object Oriented Python

import csv
from ShopErrors import BudgetTooLowError
import ShopFunctions

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

    def setUnitPrice(self, price):
        self.product.setPrice(price)

    def getProduct(self):
        return self.product

    #defining function to get the total cost of of all the products in stock  
    def getCost(self):
        return self.getUnitPrice() * self.quantity

    def getQty(self):
        return self.quantity

    # Change incrementally the stock qty by the asked sales Qty
    def changeQty(self, askedSalesQty):
        self.quantity += askedSalesQty



    def setQty(self, newQty):
        self.quantity = newQty

    # print function: Returns the Name of the product and it's stock level        
    def __repr__(self):
        return "{}, STOCK QUANTITY: {:3d}".format(self.product, self.quantity)


class ShoppingListItem(ProductStock):

        # Constructor function (takes objects of Product class and quantity)
    def __init__(self, product, quantity):

        super().__init__(product, quantity)
        
        # Additionaly to the shopping list, the Customer will also use the shopping basket and shopping bag
        self.basket_qty = 0
        self.bag_qty = 0

    def __repr__(self):

        return "{}, REQUIRED QUANTITY: {:3d}, IN THE BASKET: {:3d}, IN THE BAG: {:3d},".format(self.product, self.quantity, self.basket_qty, self.bag_qty)       

    # function to change the quantity of the product in the basket
    def changeBasketQty(self, qty):
        self.basket_qty += qty


    # if payment was successfull, move items form the shopping basket to customers bag
    def pack_purchased_items(self):
        self.bag_qty = self.basket_qty
        self.basket_qty = 0   

    #defining function to get the cost of products in the basket
    # if there are no products in the basket, get price of products in the shopping list
    def getCost(self):
        if self.basket_qty > 0:
            cost = self.getUnitPrice() * self.basket_qty
        else:
            cost = self.getUnitPrice() * self.bag_qty

        return cost

# Define the Customer class
class Customer:

    # Constructor function
    # needs customer name and the budget
    def __init__(self, path="", name="", budget=0):

        # Shopping list: list of Products to buy, quantities in shopping basket and shopping bag
        self.shopping_list = []

        # variable to count all the products in the basket
        self.basket_qty = 0

        # variable to count the cost of purchased items
        self.payed = 0        

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

    #def itemsNotInBasketOrBag(sl):



    # function to look for items from the customre shopping list in the shops stock,
    # putting found items to the shopping basket and calculating the total cost
    # class Customer
    def fill_shopping_basket(self, shop, ef_path):

        # Loop over the customers shopping list. Filter shopping list for products that have basket_qty==0
        # Filter as per https://stackoverflow.com/questions/29051573/python-filter-list-of-dictionaries-based-on-key-value
        # The filtering is done to loop only over new products (products not yet in the basket or the shopping bag)
        for list_item in list(filter(lambda d: d.basket_qty + d.bag_qty == 0 , self.shopping_list)):
            # loop over the products in the shops stock
            for stock_item in shop.stock:

                # If product from shopping list is found in the shops stock, put it in the basket
                if list_item.getName() == stock_item.getName():
                    
                    # make sure shop has enough stock to fulfill the order
                    if stock_item.getQty() >= list_item.getQty():
                        qty = list_item.getQty()              
                    else:
                    # if it doesn't, put in the basket whatever is left in stock
                        qty = stock_item.getQty() 
                        err_msg = "There is not enough {} in stock. Actual stock: {} / Required Stock {} ".format(
                            list_item.getName(), 
                            qty, 
                            list_item.quantity
                            )
                        ShopFunctions.addToExceptionsFiles(ef_path, err_msg)

                    # keep a tally of sum of all the products in the basket
                    self.basket_qty += qty
                    
                    # Remove required qty from the shops stock
                    stock_item.changeQty(-qty)

                    # put the required amount of selected product into the shopping basket
                    list_item.changeBasketQty(qty)

                    # Assign the price 
                    list_item.setUnitPrice(stock_item.getUnitPrice())


    def addItemToShoppingList(self, prodName, unitPrice, quantity):
        # Add new product to the shopping list
        p = Product(prodName, unitPrice)
        self.shopping_list.append(ShoppingListItem(p, quantity))



    # function to calculate the total cost of the customers order
    # class Customer
    def getOrder_cost(self):
        cost = 0
        
        # loop over the shopping list and sum the costs of each items
        for list_item in self.shopping_list:
            cost += list_item.getCost()
        
        return cost

    # class Customer
    def getName(self):
        return self.name

    #class Customer
    def getShoppingList(self):
        return self.shopping_list

    # class Customer
    def setTransactionCompleted(self):
        self.transactionCompleted = True

    # Method to finilize the transaction
    # If the funds are sufficient, Customer budget is decreased by the cost of the items 
    # If the budget is too low, BudgetTooLowError is raised
    # class Customer 
    def payForItem(self, amountDue, shop):

        if self.budget >= amountDue:
            self.budget -= amountDue
            shop.acceptPayment(amountDue)
        else:
            raise BudgetTooLowError

    
    # Print customer function
    # class Customer
    def __repr__(self):
        

        str =  "{} has €{:.2f} in cash\n".format(self.name, self.budget)
        str += "Shopping list: ".format(self.name)

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

        if self.basket_qty> 0:
            str += "\nThe total cost would be: €{:.2f}, he would have €{:.2f} left\n".format(self.getOrder_cost(), self.budget-self.getOrder_cost())
        else:
            str += "\nThe total cost of purchased items: €{:.2f}. There is €{:.2f} left\n".format(self.getOrder_cost(), self.budget)

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
        str+= "Stock:\n"
        for item in self.getStock():
            str += "{}\n".format(item)
        return str

    # Define function to add stock item to Shops stock
    def addToStock(self, stock_item):
        self.stock.append(stock_item)

    # Define function to retrieve Shops stock items
    def getStock(self):
        return self.stock

    def acceptPayment(self, payment):
        self.cash += payment

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
    def performSales(self, customer, ef_path):

        # Sum cost of all items to clalculate the total transaction cost
        # transactionCost = 0

        # loop over the customers shopping list (array of ShoppingListItem Class Objects)
        for basket_item in customer.getShoppingList():


            # loop until items are in the shopping basket
            while basket_item.basket_qty > 0:

                # attempt to pay for the items. If customer has not enough cash, error will be raised
                try:
                     customer.payForItem(basket_item.getCost(), self)
                     # if payment was successfull, move items form the shopping basket to customers bag
                     basket_item.pack_purchased_items()

                except BudgetTooLowError:
                    err_msg = "{} has not enough money to pay for {} units of {} worth {:.2f} as he/she has only {:.2f}".format(
                                    customer.getName(), 
                                    basket_item.basket_qty, 
                                    basket_item.getName(), 
                                    basket_item.getCost(),
                                    customer.budget  
                                )
                    ShopFunctions.addToExceptionsFiles(ef_path, err_msg)                      

                    # remove one item from the basket
                    basket_item.changeBasketQty(-1)
                    # find the product in the shop and return one item from the basket back to the shop
                    for product in self.getStock():
                        if product.getName() == basket_item.getName():
                            product.changeQty(1)
                            break
        
        # set the number of items in basket for customer to 0
        # we know it will be zero, because we'll loop over all the items and execute internal loop until basket_qty is 0
        customer.basket_qty = 0