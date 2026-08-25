#include <stdio.h>
int main () {
    int t;
    scanf("%d", &t);
    while (t--) {
        char str[ 10001];
        scanf("%s", &str);
        int cp=0, sm = 0, dg= 0;
        for (int i = 0; i < strlen(str); i++) {
            if(str[i] >= 'A' && str[i]<='Z') cp++;
            else if (str[i] >= 'a' && str[i]<='z') sm++;
            else dg++;
        }
        printf("%d %d %d\n", cp, sm, dg);
    }
    return 0;
}