#include <stdio.h>
int main () {
    char a;
    scanf("%c", &a);
    if (a >= 48 && a<= 57) printf("IS DIGIT\n");
    else {
        printf("ALPHA\n");
        if(a >= 'A' && a <= 'Z') printf("IS CAPITAL\n");
        else printf("IS SMALL\n"); 
    }
    return 0;
}