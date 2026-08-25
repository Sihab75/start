#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n,k;
        cin >> n >> k;
        string s;
        cin >> s;
        int cnt = count(s.begin(), s.end(), '1');
        int l = 0;
        int r = k-1;
        int ans = cnt;
        while(r<n) {
            int ad = cnt-count(s.begin()+l, s.begin()+r+1, '1')+k;
            ans = max(ans, ad);
            r++;
            l++;
        }
        cout << ans << '\n';
    }
    return 0;
}