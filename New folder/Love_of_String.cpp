#include<bits/stdc++.h>
using namespace std;

int main () {
    int n, k;
    cin >> n >> k;
    string s;
    cin>>s;
    int l = 0;
    int r = k-1;
    string ans = s;
    while(r<n) {
        string temp = s;
        sort(temp.begin()+l,temp.begin()+r+1);
        ans = min(ans, temp);
        r++;
        l++;
    }
    cout << ans<< "\n";
    return 0;
}