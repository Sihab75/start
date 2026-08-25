#include <stdio.h>
int main () {
    int t;
    scanf("%d", &t);
    while (t--) {
        long long n, a, b, c;
        scanf("%lld %lld %lld %lld", &n, &a, &b, &c);
        if ((n%(a*b*c)) != 0) {
            printf("%d\n", -1);
        } else {
            printf("%lld\n", (n/(a*b*c)));
        }
    }
    return 0;
}