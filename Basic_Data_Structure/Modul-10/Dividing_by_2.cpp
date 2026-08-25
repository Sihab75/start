#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for(int i = 0; i < n;++i) {
            cin >> a[i];
        } 
        sort(a.begin(), a.end());
        int ans = 0;
        while(a[0]<a[n-1]) {
            a[n-1] /=2;
            ans++;
            sort(a.begin(), a.end());
        }
        cout<<ans << '\n';
    }
    return 0;
}