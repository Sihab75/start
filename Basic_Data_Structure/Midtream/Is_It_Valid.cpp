#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    while(t--) {
        string s;
        cin >>s;
        stack<char> st;
        for(auto ch: s) {
            st.push(ch);
        }
        int count0 = 0;
        int count1 = 0;
        while (!st.empty()) {
            if(st.top() == '1') {
                count1++;
            } else{
                count0++;
            }
            st.pop();
        }
        cout << (count0 == count1? "YES": "NO") << '\n';
    }
    return 0;
}