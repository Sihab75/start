#include<bits/stdc++.h>
using namespace std;

int main () {
    int n;
    cin >> n;
    vector<int> a(n);
    for(int i = 0; i < n;i++) {
        cin >> a[i];
    }
    sort(a.begin(), a.end());
    int count = 0;
    for(int i = 0; i < n-1; i++) {
        int tar = a[i]+1;
        int st = 0, end = n-1;
        while (st<=end) {
            int mid = st+ (end-st)/2;
            if(a[mid]>tar) {
                end = mid -1;
            } else if (a[mid]<tar) {
                st=mid+1;
            } else {
                count++;
                break;
            }
        }
    }
    cout << count << '\n';
    return 0;
}