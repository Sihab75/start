#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for(auto &x: a) cin >> x;
        for(int i = 0; i<n; i++) {
            int n;
            string s;
            int count = 0;
            cin >> n >> s;
            for(auto ch: s) {
                if(ch=='D') count++;
                else count--;
            }
            a[i] = (a[i]+count%10+10)%10;
        }
        for(auto x: a) cout << x<<' ';
        cout << '\n';
    }
    return 0;
}