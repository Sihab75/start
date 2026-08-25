#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int>a(n);
        int mx = INT_MIN;
        int mi = INT_MAX;
        for(int i = 0; i < n;i++) {
            cin >> a[i];
            mx = max(a[i], mx);
            mi=min(a[i], mi);
        }
        cout << mx-mi+1 << '\n';
    }
    return 0;
}