#include <stdio.h>
int main () {
    long long n;
    scanf ("%lld", &n);
    if(n>= 1500) {
        printf("I will buy Punjabi\n");
        printf("I will buy new shoes\n");
        printf("Alisa will buy new shoes\n");
    } else if(n > 1000) {
        printf("I will buy Punjabi\n");
    } else {
        printf("Bad luck!\n");
    }
    return 0;
}