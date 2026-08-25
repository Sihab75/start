#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }
        int count  = 0;
        for(int i = 0; i < n; i++) {
            int lcount = 0;
            int rcount = 0;
            for(int l = i-1;l>=0; l--) {
                if(a[i]>a[l]) {
                    lcount++;
                } 
            }
            for(int r = i+1; r<n; r++) {
                if(a[r]>a[i]) {
                    rcount++;
                }
            }
            if(lcount==rcount) {
                count++;
            }
        }
        cout << count << '\n';
    }
    return 0;
}