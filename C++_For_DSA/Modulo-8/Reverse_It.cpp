#include<bits/stdc++.h>
using namespace std;

class Student{
public:
    string nm;
    int cls;
    char s;
    int id;
};

int main () {
    int n;
    cin >> n;
    Student st[n];
    vector<char> sec(n);
    for(int i = 0; i < n; i++) {
        cin >> st[i].nm >> st[i].cls >> st[i].s >> st[i].id;
        sec[i]=st[i].s;
    }
    reverse(sec.begin(),sec.end());
    for(int i = 0; i < n;i++) {
        st[i].s = sec[i];
    }
    for(int i = 0; i < n;i++) {
        cout << st[i].nm << ' ' << st[i].cls << ' ' << st[i].s << ' ' << st[i].id << '\n';
    }
    
    return 0;
}