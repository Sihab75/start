#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n, p;
        cin >> n >> p;
        int cost1 = 0;
        int cost2 = 0;
        vector<char> a(n);
        for(int i = 0;i < n; i++) {
            cin >> a[i];
        }
        for(int i = p-1; i<n; i++) {
            if(a[i]=='L') {
                cost1++;
            }
        }
        for(int i = p-1; i>=0; i--) {
            if(a[i]=='R') {
                cost2++;
            }
        }
        cout << min(cost1, cost2) << '\n';
    } 
    return 0;
}