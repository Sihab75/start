#include<bits/stdc++.h>
using namespace std;
int vowel(string s, int count, int i) {
    if(s.size() == i) return count;
    if(s[i] =='a' || s[i]=='e' || s[i]=='i' || s[i]=='o' || s[i]=='u'){
        count++;
    }
    return vowel(s, count, i+1);
}
int main () {
    string s;
    getline(cin, s);
    for(char &ch: s) {
        ch = tolower(ch);
    }
    cout<< vowel(s, 0, 0) << '\n';
}