#include<bits/stdc++.h>
using namespace std;

int main () {
    string s;
    cin >> s;
    vector<int> freq(26,0);
    for(auto ch: s) {
        freq[ch-'a']++;
    }
    for(int i = 0;i < 26; i++) {
        if (freq[i]!=0)
        cout << (char)(i+'a') << " : " << freq[i] << '\n';
    }
    return 0;
}