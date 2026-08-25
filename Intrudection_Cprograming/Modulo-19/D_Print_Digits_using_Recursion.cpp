#include<bits/stdc++.h>
using namespace std;

void printDigit(int n) {
    if(n==0) return;
    printDigit(n/10);
    cout<< n%10 << ' ';
}


int main () {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        if (n==0) {
            cout<<n << '\n';
        } else {
            printDigit(n);
            cout << '\n';
        }
    }
    return 0;
}