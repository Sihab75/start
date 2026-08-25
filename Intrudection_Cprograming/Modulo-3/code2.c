#include <stdio.h>
int main () {
    int a;
    long long b;
    float c;
    char ch;
    scanf("%d %lld %f %c", &a, &b, &c,&ch);
    printf("%d\n%lld\n%.2f\n%c\n", a, b, c, ch);
    return 0;
}