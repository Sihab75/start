#include<bits/stdc++.h>
using namespace std;

int main () {
    int n;
    cin >> n;
    vector<long long> a(n);
    long long sum = 0;
    for(auto &x: a){
       cin >> x; 
        sum+=x;
    } 
    sort(a.begin(), a.end());
    for(auto &x: a) {
        if((sum&1)==0) break;
        if(x&1)sum-=x;
    }
    cout << sum << '\n';
    return 0;
}