#include<bits/stdc++.h>
using namespace std;

int main () {
    int a, b,c;
    cin >> a>> b>>c;
    int i = 0;
    int ans = -1;
    while (c*i<=b) {
        if(a<=c*i && c*i<=b) {
            ans = c*i;
            break;
        }
        i++;
    }
    cout << ans << '\n';
    return 0;
}