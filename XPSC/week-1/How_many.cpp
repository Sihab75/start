#include<bits/stdc++.h>
using namespace std;
long long ans;

int main () {
    long long s, t;
    ans = 0;
    cin >> s >> t;
    for(int i = 0; i <=s; i++) {
        for(int j = 0; j <=s; j++) {
            for(int k = 0; k<=s; k++) {
                if(i+j+k<=s&&i*j*k<=t) {
                    ans++;
                }
            }
        }
    }
    cout << ans << '\n';
    return 0;
}