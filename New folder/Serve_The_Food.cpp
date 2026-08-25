#include<bits/stdc++.h>
using namespace std;

int main () {
    int t;
    cin >> t;
    queue<int> q;
    while (t--) {
        int x;
        cin >> x;
        if(x==1) {
            int val;
            cin >> val;
            q.push(val);
        }else {
            if(q.empty()) {
                cout << -1<< '\n';
            } else {
                cout << q.front() << '\n';
                q.pop();
            }
        }
    }
    return 0;
}