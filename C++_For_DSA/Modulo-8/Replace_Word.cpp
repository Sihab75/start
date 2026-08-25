#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while (t--) {
        string s, x;
        cin >> s >> x;
        while (s.find(x)!=string::npos) {
            s.replace(s.find(x),x.size(), "#");
        }
        cout << s << '\n';
    }
    return 0;
}