#include<bits/stdc++.h>
using namespace std;
#define ina(a) for(auto &x: a) cin >> x
#define pa(a)  for(auto &x: a) cout << x << ' '
#define nl  cout << '\n'
#define ll long long
#define vi vector<ll>
#define vii vector<vector<ll>>

void now(){
    ll n, x, y;
    cin >> n >> x >> y;
    if(n<=3) {
        cout << n*x;
        nl;
        return;
    }
    ll costx = x*3;
    ll costy = y*(n-3);
    cout << costx+costy;
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