#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>

struct Product{
    char* name;
    double price;
};

struct ProductStock{
    struct Product product;
    int quatity;
};

struct Customer{
    char* name;
    double budget;
    struct ProductStock shoppingList[20];
    struct ProductStock shoppingBasket[20];
    struct ProductStock shoppingBag[20];
    int index;
};

struct Shop
{
    double cash;
    struct ProductStock stock[20];
    int index;
};

struct transactionParties
{
    struct Shop shop;
    struct Customer customer;
};

void printProduct(struct Product p){
    printf("NAME: %s, PRICE:  €%.2f", p.name, p.price);
}

void printCustomer(struct Customer c){

    double totalCost = 0;

    printf("\n");
    printf("%s has €%.2f in cash\n", c.name, c.budget);

    for(int i=0; i<c.index; i++){
        printProduct(c.shoppingBasket[i].product);
 
        printf(", REQUIRED QUANTITY: %d", c.shoppingList[i].quatity);
        printf(", IN THE BASKET: %d", c.shoppingBasket[i].quatity);
        printf(", IN THE BAG: %d\n", c.shoppingBag[i].quatity);
        double cost = c.shoppingBasket[i].product.price*c.shoppingBasket[i].quatity;
        totalCost +=cost;
        //printf("Cost of this order is %.2f\n\n", cost);
    }

    double rest = c.budget - totalCost;
    printf("------------------------------------------\n");
    printf("The total cost would be €%.2f, customer would have €%.2f left\n\n", totalCost, rest);
}

struct Customer readCustomerFromFile(char *custFile)
{
    //struct Customer cust;

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen(custFile, "r");
    if(fp==NULL){
        exit(EXIT_FAILURE);
    }

    //read firts line with customres name an budget
    read = getline(&line, &len, fp);

    char *n = strtok(line, ",");
    char *b = strtok(NULL, ",");

    char *custName = malloc(sizeof(char)*50);
    strcpy(custName, n);

    float custBudget = atof(b);

    struct Customer cust = {
        custName,
        custBudget
    };


    // read the shopping list
    while((read = getline(&line, &len, fp)) !=-1){

        char *n = strtok(line, ",");
        char *q = strtok(NULL, ",");

        int quantity = atoi(q);

        char *name = malloc(sizeof(char)*50);
        strcpy(name, n);

        struct Product product = 
        {
            name,
            0
        };         

        struct ProductStock stockItem =
        {
            product,
            quantity
        };

        cust.shoppingList[cust.index++]=stockItem;        
    }

    return cust;
};


struct Shop createAndStockShop(char *stockFile){
    struct Shop shop = {200};

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;


    fp = fopen(stockFile, "r");
    if(fp==NULL){
        exit(EXIT_FAILURE);
    }

    //read the first line with shops cash
    read = getline(&line, &len, fp);

    // assign value from the first line as a shops cash
    shop.cash = atof(line);

    printf("Shops budget: %f \n", shop.cash);

    // add the products to the stock. 
    // Read them from line 2 onwards
    while((read = getline(&line, &len, fp)) !=-1){
        //printf("line: %s", line );
        //printf("lines length: %zu:\n", read);

        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");

        int quantity = atoi(q);
        float price = atof(p);

        char *name = malloc(sizeof(char)*50);
        strcpy(name, n);

        struct Product product = 
        {
            name,
            price
        }; 
        
        struct ProductStock stockItem =
        {
            product,
            quantity
        };

        shop.stock[shop.index++]=stockItem;

    }
/*     struct stat sb;


    char *textRead = malloc(sb.st_size);
    int i = 0;



    //scans over each line if the file fp
    while (fscanf(fp, "%[^\n] ", textRead) != EOF){


        if(i==0){
 
        }
        else{

             breaks string into a series of tokens using delimiter ','
            char *n = strtok(textRead, ",");        

            char *name = malloc(sizeof(char)*50);
            printf("%s, %d\n", n, i);
            strcpy(name, n);

            float price = atof(strtok(NULL, ","));
            int quantity = atoi(strtok(NULL, ","));

            struct Product product = {name, price};
            struct ProductStock stockItem = {product, quantity};

            shop.stock[shop.index++] = stockItem;
        }

        i++;
    }  */ 

    fclose(fp);

    return shop;
}

void printShop(struct Shop s){
    printf("shop has €%.2f in cash\nStock:\n", s.cash);    

    for(int i=0; i<s.index; i++){
        printProduct(s.stock[i].product);
        printf(", STOCK QUANTITY: %d \n", s.stock[i].quatity);
    }
}

//function to fill the customser's shopping basket
struct transactionParties fillShoppingBasket(struct transactionParties tp){

    for(int i=0; i<tp.customer.index; i++){
        for(int j=0; j<tp.shop.index; j++){
            //compare product names from customer list and shops stock
            if( strcmp(tp.customer.shoppingList[i].product.name, tp.shop.stock[j].product.name)==0){

                int transactionQty = 0;
                if(tp.shop.stock[j].quatity >= tp.customer.shoppingList[i].quatity){
                    transactionQty = tp.customer.shoppingList[i].quatity;
                }else{
                    transactionQty = tp.shop.stock[j].quatity ;
                }
                // Add product to the basket
                struct ProductStock basketItem = {
                    tp.shop.stock[j].product,
                    transactionQty
                };
                //update the shops stock                    
                tp.shop.stock[j].quatity = tp.shop.stock[j].quatity - transactionQty;


                tp.customer.shoppingBasket[i] = basketItem;

            }
        }
    }

    return tp;
}


struct transactionParties finalizeTransaction(struct transactionParties tp){

    printf("Press ENTER to finalize the sale\n");
    char ch;
    scanf("%c", &ch);
    scanf("%c", &ch);

    return tp;
}

//function to display the Options menu for the end user
void displayMainMenu(){
    system("clear");
    printf("MAIN MENU \n");

    printf("1---Read Shopping list from file \n");
    printf("2---Live mode \n");
    printf("0---Exit \n");
    printf("\n");

}

void readFromFile(struct Shop s){
    //system("clear");
    struct Customer c = readCustomerFromFile("customer.csv");

    struct transactionParties tp={
        s, c
    };

    printf("Shop an the Customer pre-transaction: \n\n");
    tp = fillShoppingBasket(tp);
    //print the shop and customer status before the transaction
    printShop(tp.shop);
    printCustomer(tp.customer);
    //execute the transaction
    tp = finalizeTransaction(tp);
}



void liveMode(){
    printf("Option 2 \n");
}

int main(void)
{
    struct Customer przemek={"Przemek", 100.0};

    struct Product coke={"Can of Coke", 1.10};
    struct Product bread={"Bread", 0.7};

    struct ProductStock cokeStock = {coke, 20};
    struct ProductStock breadStock = {bread, 2};


    struct Shop myShop = createAndStockShop("stock.csv");

    // initialize variable
    int userInput = -1;  

    displayMainMenu();

    while(userInput!=0){
        printf("Enter your choice: ");
        scanf("%d", &userInput);

        if(userInput==1){
            readFromFile(myShop);
        } else if(userInput==2){
            liveMode();
        }
        else if(userInput==0){
            printf("Exiting \n");
        }else{
            displayMainMenu();
        }
    }


    //printProduct(coke);

    //przemek.shoppingList[przemek.index++] = cokeStock;
    //przemek.shoppingList[przemek.index++] = breadStock;

    //printCustomer(przemek);

    return 0;
}