#include <iostream>
using namespace std;

void recursion(int n) {
    if (n==0) return;
    cout << "I love Recursion" << '\n';
    recursion(--n);
}

int main () {
    int n;
    cin >> n;
    recursion(n);
    return 0;
}