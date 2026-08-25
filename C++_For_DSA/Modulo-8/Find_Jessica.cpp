#include<bits/stdc++.h>
using namespace std;

int main () {
    string s;
    bool flag = false;
    while(cin >> s) {
        if(s=="Jessica") {
            flag = true;
            break;
        }
    }
    cout << (flag?"YES":"NO") << '\n';
    return 0;
}