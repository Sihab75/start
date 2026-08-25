#include <bits/stdc++.h>
using namespace std;
int main () {
    int n;
    cin >> n;
    int arr[n];\
    int mi = INT_MAX;
    for(int i= 0; i < n;i++) {
        cin >> arr[i];
        mi = min(arr[i],mi);
    }
    map <int, int> mp;
    for(auto val: arr) {
        mp[val]++;
    }
    cout << ((mp[mi]&1) == 0? "Unlucky": "Lucky") << '\n';
    return 0;
}