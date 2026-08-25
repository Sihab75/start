#include <stdio.h>
#include <string.h>
int is_palindrome(char str[]) {
    int n = strlen(str);
    int st =0, end = n-1;
    int isPalicdrom = 1;
    while (st<=end) {
        if(str[st] != str[end]) {
            isPalicdrom=0;
            break;
        }
        st++;
        end--;
    }
    return isPalicdrom;
}
int main () {
    char str[1001];
    scanf("%s", &str);
    if(is_palindrome(str)==1) {
        printf("Palindrome\n");
    } else {
        printf("Not Palindrome\n");
    }
    return 0;
}