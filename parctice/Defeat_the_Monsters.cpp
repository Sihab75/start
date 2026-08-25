#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int a, b, c;
        cin >> a >> b >> c;
        while(a-1>=0 && b-2>=0) {
            a--;
            b-=2;
        }
        while(b-1>=0 && c-2>=0) {
            b--;
            c-=3;
        }
        cout << ((a==0)&&(b==0)&&(c==0)? "Yes":"No") << '\n';
    }
    return 0;
}