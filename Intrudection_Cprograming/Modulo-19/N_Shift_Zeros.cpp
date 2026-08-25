#include <bits/stdc++.h>
using namespace std;

void shifitArray(int arr[], int n) {
    int arr2[n] = {0};
    int k = 0;
    for(int i = 0; i < n;i++) {
        if (arr[i]!=0) {
            arr2[k] = arr[i];
            k++;
        }
    }
    for (auto val: arr2) {
        cout << val << " ";
    }
    cout << '\n';
}

int main () {
    int n;
    cin >> n;
    int arr[n];
    for(int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    shifitArray(arr, n);
    
    return 0;
}