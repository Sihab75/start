#include <bits/stdc++.h>
using namespace std;

int main () {
    int n;
    cin >> n;
    int mat[n][n];
    for(int row = 0; row<n;row++) {
        for(int col = 0; col<n; col++){
            cin>> mat[row][col];
        }
    }
    long long sumP = 0;
    long long sumS = 0;
    for(int row = 0; row<n; row++) {
        for(int col = 0; col <n;col++) {
            if(col==row ) sumP += 1LL * mat[row][col];
            if(row+col == n-1) sumS += 1LL * mat[row][col];
        }
    }
    long long sum = abs(sumP-sumS);
    cout << sum<<'\n';
    return 0;
}