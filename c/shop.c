#define _GNU_SOURCE
#include <stdio.h>
#include <time.h>
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

    double totalCostDue = 0;
    double totalCostPayed = 0;
    int itemsInBasket = 0;
    int itemsInBag = 0;

    printf("\n");
    printf("%s has €%.2f in cash\n", c.name, c.budget);

    for(int i=0; i<c.index; i++){

        //Count total items in the basket and in the bag
        itemsInBasket += c.shoppingBasket[i].quatity;
        itemsInBag += c.shoppingBag[i].quatity;

        printProduct(c.shoppingBasket[i].product);
 
        printf(", REQUIRED QUANTITY: %d", c.shoppingList[i].quatity);
        printf(", IN THE BASKET: %d", c.shoppingBasket[i].quatity);
        printf(", IN THE BAG: %d\n", c.shoppingBag[i].quatity);

        totalCostPayed += c.shoppingBag[i].product.price*c.shoppingBag[i].quatity;
        totalCostDue += c.shoppingBasket[i].product.price*c.shoppingBasket[i].quatity;
        //printf("Cost of this order is %.2f\n\n", cost);
    }

    if(itemsInBasket > 0){
        double rest = c.budget - totalCostDue;
        printf("------------------------------------------\n");
        printf("The total cost would be €%.2f, customer would have €%.2f left\n\n", totalCostDue, rest);        
    } else if(itemsInBag > 0){
        printf("------------------------------------------\n");
        printf("The total cost of purchased items: €%.2f. Customer has €%.2f left\n\n", totalCostPayed, c.budget);
    }

}

struct Customer readCustomerFromFile(const char *custFile)
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

// Function to create Shop with a stock from a file
struct Shop createAndStockShop(const char* stockFile){
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

// function to log the exceptions to the file
void logException(const char* log_file, char* log_text){
    
    // file pointer
    FILE * fp;
    // current time
    time_t result = time(NULL);

    //https://stackoverflow.com/questions/41705537/how-to-remove-line-breaks-after-ctime-in-c-program
    char *t = ctime(&result);
    if (t[strlen(t)-1] == '\n') t[strlen(t)-1] = '\0';

    // open the log file
    fp = fopen(log_file, "a");
    if(fp == NULL){
        printf("Couldn't open file\n");
    return;
    }
    //write the exception log with the current time stamp
    fprintf(fp, "%s, %s\n", t, log_text);
    // close the file
    fclose(fp);
}

//function to fill the customser's shopping basket
struct transactionParties fillShoppingBasket(struct transactionParties tp, const char* log_file){

    for(int i=0; i<tp.customer.index; i++){
        for(int j=0; j<tp.shop.index; j++){
            //compare product names from customer list and shops stock

            int compareNames = strcmp(tp.customer.shoppingList[i].product.name, tp.shop.stock[j].product.name);
            
            //if product was found in the shops stock
            // and was not bought already
            if( compareNames == 0 && tp.customer.shoppingBag[i].quatity==0){

                int transactionQty = 0;
                //check shops stock
                if(tp.shop.stock[j].quatity >= tp.customer.shoppingList[i].quatity){
                    transactionQty = tp.customer.shoppingList[i].quatity;
                }else{
                    // https://stackoverflow.com/questions/4881937/building-strings-from-variables-in-c
                    char *msgOut;
                    asprintf(&msgOut, "There is not enough %s in stock. Actual stock: %i / Required Stock %i", 
                    tp.customer.shoppingList[i].product.name, tp.shop.stock[j].quatity, tp.customer.shoppingList[i].quatity);
                    logException(log_file, msgOut);
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

                // Exit internal for loop if product was found and added to basket
                break;

            }else if(j==tp.shop.index-1){ //if product from shopping list is not found, add 0 stock of it to the basket
                // Add product to the basket
                struct ProductStock basketItem = {
                    tp.customer.shoppingList[i].product,
                    0
                };

                tp.customer.shoppingBasket[i] = basketItem;                
            }
        }
    }

    return tp;
}


struct transactionParties finalizeTransaction(struct transactionParties tp, const char* log_file){

    
    printf("Press ENTER to finalize the sale\n");
    //char ch;
    // Read the input to give user a chance to read the Customer and shop status
    //scanf("%c", &ch);
    getchar();
    //scanf("%c", &ch);
    //getchar();

    //loop over the items in the basket to try to pay for them individually

    for(int i=0; i<tp.customer.index; i++){

        while (tp.customer.shoppingBasket[i].quatity > 0)
        {
            float payment_due = tp.customer.shoppingBasket[i].quatity * tp.customer.shoppingBasket[i].product.price;

            // Check if the customer has enough cash to pay for all the items
            if(tp.customer.budget > payment_due){

                //pay for the items
                tp.customer.budget = tp.customer.budget  - payment_due;
                tp.shop.cash = tp.shop.cash + payment_due;

                struct ProductStock bagItem = {
                    tp.customer.shoppingBasket[i].product,
                    tp.customer.shoppingBasket[i].quatity 
                };

                tp.customer.shoppingBag[i] = bagItem;

                /*struct ProductStock basketItem = {
                    tp.customer.shoppingBasket[i].product,
                    0
                };*/

                tp.customer.shoppingBasket[i].quatity = 0;
            }else{
                //if customer can't afford to pay for all the items, remove one item from the basket

                float cost = tp.customer.shoppingBasket[i].product.price * tp.customer.shoppingBasket[i].quatity;
                char *msgOut;
                asprintf(&msgOut, "%s has not enough money to pay for %i units of %s worth %.2f as he/she has only %.2f", 
                tp.customer.name, tp.customer.shoppingBasket[i].quatity, tp.customer.shoppingBasket[i].product.name, cost, tp.customer.budget);
                logException(log_file, msgOut);

                for(int j=0; j<tp.shop.index; j++){

                    //compare product names from customer list and shops stock
                    if(strcmp(tp.customer.shoppingList[i].product.name, tp.shop.stock[j].product.name) ==0 ){
                        tp.customer.shoppingBasket[i].quatity -=1; 
                        // and put it back on the shelf                        
                        tp.shop.stock[j].quatity +=1;
                        break;
                    }
                }
            }
        
    }
    }  

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

//function to display the Options menu for the end user
void displayliveMenu(){
    system("clear");
    printf("LIVE SHOP MENU \n");

    printf("   3---Ask for product \n");
    printf("   4---Check the shopping cart \n");
    printf("   5---Pay for items \n");
    printf("   0---Exit \n");
    printf("\n");

}

void readFromFile(struct Shop s, const char* cust_csv_file, const char* log_file){
    //system("clear");
    struct Customer c = readCustomerFromFile(cust_csv_file);

    struct transactionParties tp={
        s, c
    };

    tp = fillShoppingBasket(tp, log_file);

    printf("Shop an the Customer pre-transaction: \n\n");
    //print the shop and customer status before the transaction
    printShop(tp.shop);
    printCustomer(tp.customer);
    //execute the transaction
    tp = finalizeTransaction(tp, log_file);
    printf("Shop an the Customer post-transaction: \n\n");
    //print the shop and customer status before the transaction
    printShop(tp.shop);
    printCustomer(tp.customer);

    printf("Press ENTER to continue\n");
    // Read the input to give user a chance to read the Customer and shop status
    //char ch;
    //scanf("%c", &ch);      
    getchar();
}



void liveMode(struct Shop s, const char* log_file){
    #define MAX_STRING_SZ 50

    char *custName = malloc(MAX_STRING_SZ);
    float custBudget;
    int userInput = -1; 

    

    printf("Please enter the Customer name: ");
    //fgets(custName, MAX_STRING_SZ, stdin);
    scanf("%s", custName);
    getchar();

    printf("Please enter the Customer budget: ");
    scanf("%f", &custBudget);
    getchar();

    //create a Customer struct

    struct Customer c = {
        custName,
        custBudget
    };

    struct transactionParties tp={
        s, c
    };


    while(userInput != 0){
        displayliveMenu();
        printf("Enter your choice: ");
        scanf("%d", &userInput);
        getchar();
        
        if(userInput == 3){
            //Ask for product
            char *prodName = malloc(MAX_STRING_SZ);
            int reqQty = 0;
            int availQty = 0;
            struct Product prod;

            printf("Please enter the product name: ");
            // fgets used to allo for strings with spaces
            fgets(prodName, MAX_STRING_SZ, stdin);

            // remove the new line character form the end of the sting
            if( (strlen(prodName)>0) && (prodName[strlen(prodName) -1 ]=='\n')){
                prodName[strlen(prodName) - 1] = '\0';
            }

            //find product in the shop
            for(int j=0; j<tp.shop.index; j++){
                //compare product names from customer list and shops stock
                if(strcmp(prodName, tp.shop.stock[j].product.name) ==0 ){
                    prod = tp.shop.stock[j].product;
                    availQty  = tp.shop.stock[j].quatity;
                    break;
                }
            }

            if(availQty == 0){
                printf("The Shop doesn't have %s in stock", prodName);
                // Read the input to give user a chance to read the Customer and shop status
                getchar();
            }else{
                printf("The shop has %i units of %s in stock. The unit price is €%.2f \n", availQty, prodName, prod.price);
                printf("Please specify the required amount: ");
                scanf("%i", &reqQty);
                getchar();

                if(reqQty > 0){
                    struct ProductStock shoppingListItem =
                    {
                        prod,
                        reqQty
                    };

                // add the item to the shopping list
                tp.customer.shoppingList[tp.customer.index++] = shoppingListItem;

                tp = fillShoppingBasket(tp, log_file);
                    
                }
            }

        } else if(userInput == 4){
            printShop(tp.shop);
            printCustomer(tp.customer);
            printf("Press ENTER to continue\n");
            // Read the input to give user a chance to read the Customer and shop status
            getchar();
        } else if(userInput == 5){
            //Pay for the products
                //execute the transaction
            tp = finalizeTransaction(tp, log_file);
            printf("Shop an the Customer post-transaction: \n\n");
            //print the shop and customer status before the transaction
            printShop(tp.shop);
            printCustomer(tp.customer);
            printf("Press ENTER to continue\n");
            // Read the input to give user a chance to read the Customer and shop status
            getchar();            
        } else{
            printf("%i is not a valid Menu option\n", userInput);
        }
    }

}

int main(void)
{
    // these won't be changed during run of the program, defining them as constants:
    const char* shop_csv_file = "../stock.csv";
    const char* cust_csv_file = "../customer.csv";
    const char* log_file = "../Exceptions.csv";

    // initializing the shop
    // Shop is initialized only once at the begining of the program
    struct Shop myShop = createAndStockShop(shop_csv_file);

    // initialize variable
    int userInput = -1;  
    
    // run this loop until user presses 0
    while(userInput!=0){
        displayMainMenu();
        printf("Enter your choice: ");
        scanf("%d", &userInput);
        getchar();

        if(userInput==1){
            readFromFile(myShop, cust_csv_file, log_file);
        } else if(userInput==2){
            liveMode(myShop, log_file);
        }
        else if(userInput==0){
            printf("Exiting \n");
        }else{
            displayMainMenu();
        }
    }

    return 0;
}