#include<bits/stdc++.h>
using namespace std;

int main () {
    int n, p, c;
    cin >> n >> p >> c;
    vector<int> a(n);
    vector<long long> pre (n);
    cin >> a[0];
    pre[0] = a[0];
    for(int i = 1; i < n; i++) {
        cin >> a[i];
        pre[i] = pre[i-1]+a[i];
    }
    
    int q;
    cin >>q;
    while(q--) {
        int l, r;
        cin >> l >> r;
        l--;
        r--;
        long long sum = pre[r] - (l > 0 ? pre[l-1] : 0);
        long long count = r - l + 1;
        cout << ((sum * p )+ (count* c)) << '\n';
    }
    return 0;
}