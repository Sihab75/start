#include <iostream>
using namespace std;


int main () {
    int t;
    cin >> t;
    while(t--) {
        int a, b;
        cin >> a >> b;
        cout << ((a%2==0 || b%2==0)? "YES": "NO") << '\n';
    }
    return 0;
}