#include<bits/stdc++.h>
using namespace std;

long long fact(int n) {
    if (n==0) return 1;
    return 1LL*n*fact(n-1);
}

int main () {
    int n;
    cin >> n;
    cout << fact(n) << '\n';
}