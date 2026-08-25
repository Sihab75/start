#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<long long> a(n);
        
        long long ans = 0;
        for(int i = 0; i < n; ++i) {
            cin >> a[i];
        }
        long long waitTime = a[0];
        for(int i=1; i<n; ++i) {
            waitTime = max(waitTime, a[i]);
            ans += waitTime-a[i];
        }
        cout << ans << '\n';
    }
    return 0;
}