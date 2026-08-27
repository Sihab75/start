#include<bits/stdc++.h>
using namespace std;
#define ina(a) for(auto &x: a) cin >> x
#define pa(a)  for(auto &x: a) cout << x << ' '
#define nl  cout << '\n'
#define ll long long
#define vi vector<ll>
#define vii vector<vector<ll>>
vii dp;

ll f(ll a, ll b, ll p, ll q, ll r) {
    if(a<0||b<0) return 1e9;
    if(a==0 && b==0) return 0;
    if(dp[a][b]!=-1) return dp[a][b];
    ll r1 =p+f(a-1, b, p, q, r);
    ll r2 = p+f(a-2, b, p, q, r);
    ll u1 = q+f(a, b-1, p, q, r);
    ll u2 = q+f(a, b-2, p, q, r);
    ll ru = r+f(a-1, b-1, p, q, r);
    return dp[a][b] = min({r1, r2, u1, u2, ru});
}

void now(){
    ll a, b, p, q, r;
    cin >> a >> b >>p >> q >> r;
    dp.assign(a+1, vi(b+1, -1));
    cout << f(a, b, p, q, r);
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