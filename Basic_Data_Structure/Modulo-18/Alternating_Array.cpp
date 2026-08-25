#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for(int i = 0; i < n; i++) {
            cin >> a[i];
        }
        int count1 = 0;
        int count2 = 0;
        for(int i = 0; i < n;++i) {
            if((i&1) == 0) {
                if((a[i]&1) == 0){
                    count1++;
                }
            }else {
                if((a[i]&1)!=0) {
                    count1++;
                }
            }
            if((i&1)==0) { 
                if((a[i]&1)!=0) {
                    count2++;
                }
            } else {
                if((a[i]&1) == 0) {
                    count2++;
                }
            }
        }
        cout<<min(count1, count2) << '\n';   
    }
    return 0;
}