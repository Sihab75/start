#include<bits/stdc++.h>
using namespace std;

int main () {
    int n;
    cin >> n;
    bool isLucky = false;
    int Lucky[] = {4, 7, 44, 47, 74, 77, 444, 447, 474, 477, 744, 747, 774, 777};
    for (auto val: Lucky) {
        if(n%val == 0) {
            isLucky = true;
            break;
        }
    }
    cout << (isLucky? "YES": "NO") << endl;
    return 0;
}