#include <stdio.h>
int main () {
    int n;
    scanf("%d", &n);
    while (n--) {
        int m1, m2, d;
        scanf("%d %d %d", &m1, &m2, &d);
        int first = m1*d;
        int total = first/(m1+m2);
        int ans = d - total;
        printf("%d\n", ans);
    }
    return 0;
}