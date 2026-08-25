#include <stdio.h>
int main () {
    int n;
    scanf("%d", &n);
    int star = 5+ n/2+1;
    for (int i= 1; i <=star; i++) {
        for (int j = 1; j <= star-i;j++) {
            printf(" ");
        }
        for(int j = 1; j <=i; j++) {
            printf("*");
        }
        for(int j = 1; j <i; j++) {
            printf("*");
        }
        printf("\n");
    }
    for ( int i = 1; i <=5; i++) {
        for (int j = 1; j <= star-n/2-1;j++) {
            printf(" ");
        }
        for(int j = 1; j  <=n; j++) {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}