#include<bits/stdc++.h>
using namespace std;

int main () {
    string s;
    cin >> s;
    char ans = '0';
    for(char ch ='a'; ch<='z'; ch++) {
        if(s.find(ch)==string::npos) {
            ans = ch;
            break;
        }
    }
    if(ans=='0') cout << "None" << '\n';
    else cout << ans << '\n';
    return 0;
}