#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--){
        int n;
        cin >> n;
        int ans =0;
        vector<int> a(n);
        for(auto &x: a) {
            cin >> x;
            if(x==1) ans++;
        }
        cout << n-ans/2 << '\n';
        // while(true){
        //     int i;
        //     sort(a.begin(), a.end());
        //     vector<int> na;
        //     int sz = a.size();
        //     if((sz&1)==0){
        //         for(i = 0; i < sz-1; i+=2) {
        //             a[i]--;
        //             a[i+1]--;
        //             ans++;
        //         }
        //         if(i==sz-1) {
        //             a[i] = 0; 
        //             ans++;
        //         }
        //         for(auto x: a) {
        //             if(x>0) na.push_back(x);
        //         }
        //         if(na.empty()) break;
        //         a.clear();
        //         a = na;
        //     } else {
        //         ans+=sz;
        //         break;
        //     }
        // }
        // cout << ans << '\n';
    }
    return 0;
}