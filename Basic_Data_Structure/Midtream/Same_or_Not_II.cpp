#include<bits/stdc++.h>
using namespace std;
class Mystack{
public:
    vector<int> a;
    void push(int val) {
        a.push_back(val);
    }
    void pop() {
        a.pop_back();
    }
    int top() {
        return a.back();
    }
    bool empty() {
        return a.empty();
    }
};
class MyQueue{
public:
    list <int> l;
    void push(int val){
        l.push_back(val);
    }
    void pop() {
        l.pop_front();
    }
    int front() {
        return l.front();
    }
    bool empty() {
        return l.empty();
    }
};
int main () {
    int n, m;
    cin >> n >> m;
    if(n!=m) {
        cout << "NO" << '\n';
        return 0;
    }
    Mystack st;
    MyQueue q;
    for(int i = 0; i < n; ++i) {
        int val;
        cin >> val;
        st.push(val);
    }
    for(int i = 0; i < m; ++i) {
        int val;
        cin >> val;
        q.push(val);
    }
    bool flag = true;
    while(!st.empty() && !q.empty()) {
        if(st.top() != q.front()) {
            flag = false;
        }
        q.pop();
        st.pop();
    }
    if(flag &&(!st.empty() && q.empty())) {
        flag = false;
    }
    cout << (flag?"YES":"NO") << '\n';
    return 0;
}