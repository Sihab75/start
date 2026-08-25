#include <stdio.h>
int main () {
    int a;
    scanf("%d", &a);
    a = a/1000;
    if((a&1) == 0) printf ("EVEN\n");
    else printf("ODD\n");
    return 0;
}