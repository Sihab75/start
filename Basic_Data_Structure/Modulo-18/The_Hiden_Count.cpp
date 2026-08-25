#include<bits/stdc++.h>
using namespace std;

int main () {
    string s;
    int k;
    cin >> s >> k;
    int n = s.size();
    int mid = n/2;
    int i = mid -k/2;
    string ans;
    while(k--) {
        ans+=s[i];
        i++;
    }
    cout << ans << '\n';
    return 0;
}