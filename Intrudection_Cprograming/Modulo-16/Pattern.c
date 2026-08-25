#include <stdio.h>
int main () {
    int n;
    scanf("%d", &n);
    for(int i =1; i <=n; i++) {
        for(int j = n-i;  j>=1; j--) {
            printf(" ");
        }
        for(int j = 1; j <=i; j++) {
            if((i&1)==0) {
                printf("-");
            }else {
                printf("#");
            }
        }
        for(int j = 1; j <=i-1; j++) {
            if((i&1)==0) {
                printf("-");
            }else {
                printf("#");
            }
        }
        for(int j = n-i - 1;  j>=1; j--) {
            printf(" ");
        }
        
        printf("\n");
    }
    for(int i =n-1; i>=1; i--) {
        for(int j = n-i;  j>=1; j--) {
            printf(" ");
        }
        for(int j = 1; j <=i; j++) {
            if((i&1)==0) {
                printf("-");
            }else {
                printf("#");
            }
        }
        for(int j = 1; j <=i-1; j++) {
            if((i&1)==0) {
                printf("-");
            }else {
                printf("#");
            }
        }
        for(int j = n-i - 1;  j>=1; j--) {
            printf(" ");
        }
        
        printf("\n");
    }
    return 0;
}