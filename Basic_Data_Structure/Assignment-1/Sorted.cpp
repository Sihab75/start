#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for(int i = 0; i < n;i++) {
            cin >> a[i];
        }
        bool flag = false;
        for(int i = 0; i < n-1; i++) {
            if(a[i]>a[i+1]) {
                flag=true;
                break;
            }
        }
        cout << (flag?"NO":"YES") << '\n';
    }
    return 0;
}