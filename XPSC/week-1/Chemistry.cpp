#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        int n,k;
        cin >> n >> k;
        string s;
        cin >> s;
        map<char, int> mp;
        for(auto ch: s) {
            mp[ch]++;
        }
        int count =0;
        for(auto it: mp) {
            if(it.second&1) count++;
        }
        cout << (count-k>1? "NO":"YES") << '\n';
    }
    return 0;
}