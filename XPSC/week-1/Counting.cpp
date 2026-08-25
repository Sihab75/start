#include<bits/stdc++.h>
using namespace std;

int main () {
    int a, b;
    cin >> a >> b;
    int ans = b-(a-1);
    cout << (ans>0? ans: 0) << '\n';
    return 0;
}