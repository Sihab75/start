#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        long long  mn = LLONG_MAX;
        vector<long long> a(n);
        for(int i = 0; i < n; i ++) {
            cin >> a[i];
        }
        vector<long long > pre(n);
        pre[0] = a[0];
        for(int i = 1; i < n;i ++) {
            pre[i]=pre[i-1]+a[i];
        }
        for(int i = 0; i < n-1; i++) {
            mn = min(mn, abs(pre[i]*2 - (pre[n-1])));
        }
        cout << mn<< '\n';
    }
    return 0;
}