#include<bits/stdc++.h>
using namespace std;

void solve(vector<int>& a, vector<int>&b) {
    vector<int> c = b;
    c.insert(c.end(),a.begin(), a.end());
    for(auto val: c){
        cout << val << ' ';
    }
}

int main () {
    int n;
    cin >> n;
    vector<int>a(n);
    vector<int>b(n);
    for(int i = 0;i < n; i++) {
        cin >> a[i];
    }
    for(int i = 0;i < n; i++) {
        cin >> b[i];
    }
    solve(a, b);
    return 0;
}