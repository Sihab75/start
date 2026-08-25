#include<bits/stdc++.h>
using namespace std;

int main () {
    int n, t;
    cin >> n >>t;
    vector<int>a;
    for(int i = 0; i < n;i++) {
        int val;
        cin >>val;
        if(val!=t) a.push_back(val);
    }
    for(auto x: a) cout << x << ' ';
    cout << '\n';
    return 0;
}