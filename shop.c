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
    int index;
};

struct Shop
{
    double cash;
    struct ProductStock stock[20];
    int index;
};

void printProduct(struct Product p){
    printf("NAME: %s, PRICE:  €%.2f", p.name, p.price);
}

void printCustomer(struct Customer c){

    double totalCost = 0;

    printf("----------------\n");
    printf("CUSTOMER NAME: %s \nCUSTOMERS BUDGET:  %.2f\n", c.name, c.budget);

    for(int i=0; i<c.index; i++){
        printf("\nProduct nr %d\n", i+1);
        printProduct(c.shoppingList[i].product);
        printf("NUMBER OF ITEMS: %d\n", c.shoppingList[i].quatity);
        double cost = c.shoppingList[i].product.price*c.shoppingList[i].quatity;
        totalCost +=cost;
        printf("Cost of this order is %.2f\n\n", cost);
    }

    printf("Total cost of %d orders is %.2f\n", c.index, totalCost);
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
        float price = atoi(p);

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
    system("clear");
    readCustomerFromFile("customer.csv");
    printf("Shop an the Customer pre-transaction: \n\n");
    printShop(s);
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