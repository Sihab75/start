#include<bits/stdc++.h>
using namespace std;
#define ina(a) for(auto &x: a) cin >> x
#define pa(a)  for(auto &x: a) cout << x << ' '
#define nl  cout << '\n'
#define ll long long
#define vi vector<ll>
#define vii vector<vector<ll>>

void now(){
    ll n;
    cin >> n;
    ll ans = n+10;
    ll mod = ans%10;
    ans = ans-mod;
    cout << ans-n;
    nl;
}
int main () {
    int t = 1;
    //cin >> t;
    while(t--) {
        now();
    }
    return 0;
}