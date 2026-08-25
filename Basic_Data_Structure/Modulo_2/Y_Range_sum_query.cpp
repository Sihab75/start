#include<bits/stdc++.h>
using namespace std;

void solve(vector<long long>& a) {
    long long x, y;
    cin >> x>> y;
    cout << (x==1? a[y-1]-0:a[y-1]-a[x-2]) << '\n';
}

int main () {
    long long n, t;
    cin >> n>> t;
    vector<long long>a(n);
    for(long long i = 0; i < n; i++) {
        cin >> a[i];
    }
    for(long long i = 1; i < n; i++) {
        a[i] +=a[i-1];
    }
    while (t--) {
        solve(a);
    }
    return 0;
}