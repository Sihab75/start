#include <stdio.h>
int main () {
    int n;
    scanf("%d", &n);
    long long sumP=0, sumN=0;
    for(int i = 0; i < n; i++) {
        int val;
        scanf("%d", &val);
        if(val > 0) {
            sumP+= ((long long) val);
        }
        else {
            sumN+= ((long long) val);
        }   
    }
  
    printf("%lld %lld\n", sumP, sumN);
    return 0;
}