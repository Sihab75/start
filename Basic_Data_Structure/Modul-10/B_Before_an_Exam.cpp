#include<bits/stdc++.h>
using namespace std;

int main () {
    int n, t;
    cin >> n >> t;
    vector<int> ans;
    while (n--) {
        int min, max;
        cin >> min >> max;
        for(int i = max; i>= min; i--) {
            if(t-i >= 0) {
                t -=i;
                ans.push_back(i);
                break;
            }
        }
    }
    if(t!=0) {
        cout << "NO" << '\n';
        return 0;
    }
    cout << "YES\n";
    for(auto val: ans) {
        cout << val << ' ';
    }
    cout << '\n';
    return 0;
}