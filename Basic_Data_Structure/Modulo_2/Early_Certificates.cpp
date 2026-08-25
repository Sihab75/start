#include<bits/stdc++.h>
using namespace std;
void solve  () {
    int n,m;
    cin >> n >> m;
    string a,b;
    cin >> a >> b;
    string s;
    int mi = min(n, m);
    for(int i = 0; i < mi;i++) {
        if(a[i]==b[i]) {
            s+=a[i];
        } else {
            break;
        }
    }
    cout << s << endl;
}
int main () {
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}