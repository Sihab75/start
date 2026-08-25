#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n;
        cin >> n;
        string s;
        cin >>s;
        int count = 0;
        bool flag = false;
        for(auto ch: s) {
            if(count==4) {
                flag = true;
                break;
            } else if(ch=='a' || ch=='e' || ch=='i' || ch=='o' || ch=='u') {
                count=0;
            } else {
                count++;
            }
        }
        if(count==4) {
            flag = true;
        }
        cout << (flag?"Yes":"No") << '\n';
    }
    return 0;
}