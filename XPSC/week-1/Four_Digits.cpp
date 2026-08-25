#include<bits/stdc++.h>
using namespace std;

int main () {
    string s;
    cin >> s;
    string ans ="";
    while(ans.size()+s.size()<4) {
        ans+='0';
    }
    ans +=s;
    cout << ans << '\n';
    return 0;
}