#include <bits/stdc++.h>
using namespace std;

void printNumber(int n) {
    if (n==1) {
        cout << n;
        return;
    }
    cout<< n << ' ';
    printNumber (--n);
}
int main () {
    int n;
    cin >> n;
    printNumber(n);
}