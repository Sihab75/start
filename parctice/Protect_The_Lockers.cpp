#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int l, r, k;
        cin >> l >> r >> k;
        int cost = 0;
        for(int i = l; i<= r; i++) {
            cost += (__gcd(i, k)==1? 1: 0);
        }
        cout << cost<< '\n';
    }
    return 0;
}