#include <bits/stdc++.h>
using namespace std;

long long l(long long n, long long count) {
    if (n<2) return count;
    return 0+l(n/2, count+1);
}

int main () {
    long long n;
    cin >> n;
    cout<< l(n, 0);
}