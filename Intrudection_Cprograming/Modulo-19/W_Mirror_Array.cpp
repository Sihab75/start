#include <bits/stdc++.h>
using namespace std;

int main () {
    int row, col;
    cin >> row >> col;
    int mat[row][col];
    for(int i = 0; i < row; i++) {
        for(int j = 0; j < col; j++) {
            cin>>mat[i][j];
        }
    }
    for(int i = 0; i < row;i++) {
        int st = 0, end = col-1;
        while(st<=end) {
            swap(mat[i][st], mat[i][end]);
            st++;
            end--;
        }
    }
    for(int i = 0; i < row; i++) {
        for(int j = 0; j < col; j++) {
            cout << mat[i][j] << ' ';
        }
        cout << '\n';
    }
    return 0;
}