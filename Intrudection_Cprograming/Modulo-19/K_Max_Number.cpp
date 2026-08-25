#include<bits/stdc++.h>
using namespace std;


int maximum(int arr[], int n, int mx, int i) {
    if (i==n) return mx;
    return maximum(arr, n, max(mx, arr[i]), i+1);
}

int main () {
    int n;
    cin >> n;
    int arr[n];
    for(int i = 0; i < n;i++) {
        cin >> arr[i];
    }
    cout << maximum(arr, n, INT_MIN, 0) << '\n';
    return 0;
}