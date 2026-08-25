#include<bits/stdc++.h>
using namespace std;

int main () {
    stack <int> s;
    int n;
    cin >> n;
    for(int i = 0; i<n; ++i) {
        int val;
        cin >> val;
        s.push(val);
    }
    stack<int> s2;
    while(!s.empty()) {
        int val = s.top();
        s.pop();
        if(s.empty()) {
            break;
        }
        s2.push(val);
    }
    
    cout<< endl;
    while(!s2.empty()) {
        cout<<s2.top() << ' ';
        s2.pop();
    }
    
    return 0;
}