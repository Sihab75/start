#include<bits/stdc++.h>
using namespace std;

int main () {
    string n;
    cin >> n;
    while(n.size()>1) {
        long long sum = 0;
        for(auto ch: n) {
            sum = sum+(ch-'0');
        }
        n = to_string(sum);
    }
    cout << n << '\n';
    return 0;
}