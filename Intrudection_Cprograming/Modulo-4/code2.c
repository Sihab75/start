#include <stdio.h>
int main () {
    int a, b;
    scanf("%d %d", &a,&b);
    long long mul = (long long) a * (long long) b;
    printf("%d\n", mul);
    return 0;
}