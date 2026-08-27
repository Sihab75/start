#include<bits/stdc++.h>
using namespace std;
#define ina(a) for(auto &x: a) cin >> x
#define pa(a)  for(auto &x: a) cout << x << ' '
#define nl  cout << '\n'
#define ll long long
#define vi vector<ll>
#define vii vector<vector<ll>>

void now(){
    ll x1, y1, x2, y2;
    cin >> x1 >> y1 >> x2 >> y2;
    if(((x1+y1)&1)!=((x2+y2)&1)){
        cout << -1;
        nl;
    }else if((x1+y1==x2+y2)||(x1-y1==x2-y2)) {
        cout << 1;
        nl;
    } else {
        cout << 2;
        nl;
    }
}
int main () {
    int t = 1;
    cin >> t;
    while(t--) {
        now();
    }
    return 0;
}