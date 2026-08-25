#include <stdio.h>
int main () {
    char str[100001];
    scanf ("%s", &str);
    int voewl = 0, con= 0;
    for (int i = 0; i < strlen(str); i++) {
        if (str[i] == 'a' ||str[i] == 'e' ||str[i] == 'i' ||str[i] == 'o' ||str[i] == 'u') {
            voewl++;
        }else {
            con++;
        }
        
    }
    printf("%d\n", con);
    return 0;
}