#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        vector<long long> a(5);
        for(int i = 0; i < 5; i++) {
            cin >> a[i];
        }
        long long sum = 0;
        for(int i =0; i< 5; i++){
            sum+= a[i];
        }
        long long mx = LONG_MIN;
        for(int i =0;  i < 5; i++) {
            mx = max(mx, a[i]-(sum-a[i]));
        }
        cout<<mx << '\n';
    }
    return 0;
}