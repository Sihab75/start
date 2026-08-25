#include <stdio.h>
int main () {
    char str[10000];
    scanf("%s", str);
    int freq[26] = {0};
    for(int i=0; i < strlen(str); i++) {
        freq[str[i]-'a']++;
    }
    for (int i = 0; i < 26; i++) {
        if (freq[i] != 0) {
            char ch = i + 'a';
            printf ("%c - %d\n", ch, freq[i]);
        }
    }
    return 0;
}