#include<bits/stdc++.h>
using namespace std;

int main () {
    int t, n;
    cin >> n>> t;
    vector<int> a(n);
    for(auto &val: a) {
        cin >> val;
    }
    while(t--) {
        int l, r;
        cin >> l >> r;
        cout << r-l << '\n';
    }
    return 0;
}