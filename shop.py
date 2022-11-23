import csv

def create_and_stock_shop():

    shop={}

    with open('stock.csv') as stock_file:
        csv_reader = csv.reader(stock_file, delimiter=',')

        first_row = next(csv_reader)
        shop["cash"]=float(first_row[0])

        shop["products"] = []

        for row in csv_reader:

            product={}

            product["name"] = row[0]
            product["price"] = float(row[1])
            product["qty"] = int(row[2])

            shop["products"].append(product)

    return shop

def read_customer():

    customer={}

    with open('customer.csv') as stock_file:
        csv_reader = csv.reader(stock_file, delimiter=',')

        first_row = next(csv_reader)

        customer["name"]=first_row[0]
        customer["cash"]=float(first_row[1])

        customer["shopping_list"] = []

        for row in csv_reader:

            product={}

            product["name"] = row[0]
            product["qty"] = int(row[1])

            customer["shopping_list"].append(product)

    return customer    


def print_product(p):
    print("Name: {}, Price: {}$, Quantity: {}".format(p["name"], p["price"], p["qty"]))
    pass

def print_shop(s):
    print("Initial cash value: {}".format(s["cash"]))
    print("Stock:")
    for product in s["products"]:
        print_product(product)


def print_customer(cust):
    print("Customer")
    print("Name: {}, Cash: {}".format(cust["name"], cust["cash"]))

    print("Shopping list:")
    for product in cust["shopping_list"]:
        print("Name: {},  Quantity: {}".format(product["name"], product["qty"]))


myShop = create_and_stock_shop()

print_shop(myShop)

customer = read_customer()

print_customer(customer)