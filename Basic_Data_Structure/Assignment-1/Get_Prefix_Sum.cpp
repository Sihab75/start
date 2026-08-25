#include<bits/stdc++.h>
using namespace std;

int main () {
    int n;
    cin >> n;
    vector<long long> a(n);
    for(int i = 0; i < n;i++) {
        cin >> a[i];
    }
    for(int i = 1; i < n; i++) {
        a[i]+=a[i-1];
    }
    reverse(a.begin(), a.end());
    for(auto val: a) {
        cout << val << ' '; 
    }
    cout << '\n';
    return 0;
}