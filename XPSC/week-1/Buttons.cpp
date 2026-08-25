#include<bits/stdc++.h>
using namespace std;

int main () {
    int a, b, ans=0;
    cin >> a >> b;
    if(a>b) {
        ans = 2*a-1;
    } else if(b>a) {
        ans = 2*b-1;
    } else {
        ans = a*2;
    }
    cout << ans << '\n';
    return 0;
}