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
    ll sum = 0;
    vi a(n);
    ina(a);
    for(int i =0; i< n; i++) {
        sum=max(sum, a[i]);
    }
    for(int i=0; i < n;i++) {
        ll select = -1;
        for(int j=0; j<i; j++) {
            if(a[i]>=a[j]) {
                select = max(select, a[j]);
            }
        }
        if(select!=-1) sum=max(sum, select+a[i]);
    }
    cout << sum;
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