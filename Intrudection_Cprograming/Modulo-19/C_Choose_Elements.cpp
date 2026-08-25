#include <bits/stdc++.h>
using namespace std;

int main () {
    int n, k;
    cin >> n >> k;
    long long arr[n];
    for(int i=0; i < n; i++) {
        cin >> arr[i];
    }
    for(int i = n-1; i> 0; i--) {
        int select = 0;
        for(int j = 1; j <=i; j++) {
            if (arr[select] > arr[j]) {
                select = j;
            }
        }
        swap(arr[i], arr[select]);
    }
    long long sum = 0;
    for (int i = 0; i < k; i++) {
        if (arr[i]<0) break;
        sum+=arr[i];
    }
    cout << sum << '\n';
    return 0;
}