#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        int mn=INT_MAX;
        for(auto &val: a) {
            cin >> val;
            mn= min(mn, val);
        }
        int cnt = count(a.begin(), a.end(), mn);
        cout << (cnt!=1?"YES":"NO") << '\n';
    }
    return 0;
}