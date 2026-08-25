#include<bits/stdc++.h>
using namespace std;

int main () {
    int n, m;
    cin >> n >> m;
    vector<int> a(n+1, -1);
    queue <int> q;
    for(int i = 0; i < m; i++) {
        int val;
        cin >> val;
        q.push(val);
    }
    for(int i=1; i <= n; i++) {
        if(!q.empty() && q.front() == i) {
            a[i] = q.front();
            q.pop();
        }
    }
    bool flag = true;

    for(int i = 1; i < n; i++) {
        if(a[i]!= -1 && a[i+1]!=-1) {
            flag = false;
        }
    }
    if(a[n]!=-1) {
        flag = false;
    }
    cout << (flag? 1:0) << endl;
    return 0;
}