#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int>a(n);
        for(int i = 0; i< n;i++){
            cin >> a[i];
        }
        int sum = 0;
        for(int i = 0; i < n;i++) {
            sum+=a[i];
        }
        bool flag = false;
        for(int i = 0; i < n; i++) {
            if(((sum-a[i])&1)==0) {
                flag=true;
                break;
            }
        }
        cout<<(flag?"Yes":"No") << '\n';
    }
    return 0;
}