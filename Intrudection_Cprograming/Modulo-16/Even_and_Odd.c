#include <stdio.h>
void odd_even()  {
    int n;
    scanf("%d", &n);
    int arr[n];
    for(int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    int countE = 0; 
    int countO =0;
    for(int i = 0; i < n;i++) {
        if((arr[i]&1) == 0) {
            countE++;
        } else {
            countO++;
        }
    }
    printf("%d %d\n", countE, countO);
}
int main () {
    odd_even();
    return 0;
}