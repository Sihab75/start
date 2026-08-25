#include <stdio.h>
int main () {
    int a,b,c;
    scanf("%d %d %d", &a, &b, &c);
    int max = a;
    int min = a;

    if(max < b || max < c) {
        if(b>c) {
            max = b;
        } else max = c;
    }
    if(min > b || min > c) {
        if(b<c) {
            min = b;
        } else min = c;
    }
    printf("%d %d\n", min, max);
    return 0;
}