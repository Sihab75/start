#include<bits/stdc++.h>
using namespace std;
#define ina(a) for(auto &x: a) cin >> x
#define pa(a)  for(auto &x: a) cout << x << ' '
#define nl  cout << '\n'
#define ll long long
#define vi vector<ll>
#define vii vector<vector<ll>>


void now(){
    ll n, k;
    cin >> n >> k;
    vi a(n);
    ina(a);
    vi pre(n);
    ll ans = 0;
    ll mx = LLONG_MIN;
    ll sum = 0;
    for(int i =0; i < n;i++) {
        mx = max(mx, a[i]);
        sum +=a[i];
        if(sum-mx<=k) ans = i+1;
    }
    cout << ans;
    nl;
}
int main () {
    int t = 1;
    cin >> t;
    while(t--) {
        now();
    }
    return 0;
}