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
    vi a(n);
    ina(a);
    ll odd =0;
    ll even = 0;
    for(int i =0; i< n; i++) {
        if(a[i]&1) odd++;
        else even++;
    }
    ll ans = 0;
    if(even<odd) ans = even*2+1;
    else if(odd<even) ans = odd*2+1;
    else ans = even*2;
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