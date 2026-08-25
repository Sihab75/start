#include<bits/stdc++.h>
using namespace std;
#define ina(a) for(auto &x: a) cin >> x
#define pa(a)  for(auto &x: a) cout << x << ' '
#define nl  cout << '\n'
#define ll long long
int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<int> a(n*2);
        ina(a);
        for(int i =0; i< n;  i++) {
            a[i] = max(a[i], a[n*2-1-i]);
        }
        ll sum=0;
        for(int i=0; i <n; i++) {
            sum+=a[i];
        }
        cout << sum;
        nl;
    }
    return 0;
}