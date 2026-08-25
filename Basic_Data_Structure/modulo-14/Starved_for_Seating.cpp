#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n, k;
        cin >> n >> k;
        vector<int> a(n);
        for(int i = 0; i< n;++i) {
            cin>>a[i];
        }
        long long ans = 0;
        
        for(int i = 0; i < n; ++i) {
            for(int j = i+1; j<n; ++j) {
                long long sum = 0;
                for(int l = 0; l < n; ++l) {
                    if(l!=i && l!=j) {
                        sum+=(a[l]/2);
                    }else {
                        sum+=a[l];
                    }
                }
                if (sum>k) {
                    ans++;
                }
            }
        }
        cout << ans << '\n';
    }
    return 0;
}