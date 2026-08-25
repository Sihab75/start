#include <stdio.h>
int main () {
    int n;
    scanf("%d", &n);
    long long sum2 = 0, sum3 = 0;
    for(int i = 0; i < n;i++) {
        int x;
        scanf("%d", &x);
        if(x%2==0) {
            sum2++;

        } else if (x%3==0) {
            sum3++;
        }
    }
    printf("%lld %lld\n", sum2, sum3);
    return 0;
}