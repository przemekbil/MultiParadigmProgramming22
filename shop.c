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
    printf("----------------\n");
    printf("PRODUCT NAME: %s \nPRODUCT PRICE:  %.2f\n", p.name, p.price);
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

struct Shop createAndStockShop(){
    struct Shop shop = {200};

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("stock.csv", "r");
    if(fp==NULL){
        exit(EXIT_FAILURE);
    }

    struct stat sb;

    char *textRead = malloc(sb.st_size);
    int i = 1;

    while (fscanf(fp, "%[^\n] ", textRead) != EOF){

        char *n = strtok(textRead, ",");

        char *name = malloc(sizeof(char)*50);
        strcpy(name, n);

        float price = atof(strtok(NULL, ","));
        int quantity = atoi(strtok(NULL, ","));

        struct Product product = {name, price};
        struct ProductStock stockItem = {product, quantity};

        shop.stock[shop.index++] = stockItem;

        i++;
    }    

    fclose(fp);

    return shop;
}

void printShop(struct Shop s){
    printf("shop has %.2f in cash\n", s.cash);

    for(int i=0; i<s.index; i++){
        printProduct(s.stock[i].product);
        printf("THE SHOP HAS %d OF THE ABOVE\n", s.stock[i].quatity);
    }
}

//function to display the Options menu for the end user
void displayMainMenu(){
    printf("MAIN MENU \n");

    printf("1---Read Shopping list from file \n");
    printf("2---Live mode \n");
    printf("0---Exit \n");
    printf("\n");

}

void readFromFile(){
    printf("Option 1 \n");
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

    int userInput = -1;

    displayMainMenu();

    while(userInput!=0){
        printf("Enter your choice: ");
        scanf("%d", &userInput);

        if(userInput==1){
            readFromFile();
        } else if(userInput==2){
            liveMode();
        }
        else if(userInput==0){
            printf("Exiting \n");
        }else{
            printf("%d is not a valid menu option \n \n", userInput);
            displayMainMenu();
        }
    }


    //printProduct(coke);

    //przemek.shoppingList[przemek.index++] = cokeStock;
    //przemek.shoppingList[przemek.index++] = breadStock;

    //printCustomer(przemek);

    //printShop(createAndStockShop());

    //printf("Hello world %c", 10);

    return 0;
}