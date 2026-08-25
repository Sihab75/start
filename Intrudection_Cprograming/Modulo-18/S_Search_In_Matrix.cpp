#include <bits/stdc++.h>
using namespace std;

int main()
{
    int row, col;
    cin >> row >> col;
    int mat[row][col];
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < col; j++)
        {
            cin >> mat[i][j];
        }
    }
    bool flag = false;
    int x;
    cin >> x;
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < col; j++)
        {
            if (mat[i][j] == x)
            {
                flag = true;
                break;
            }
        }
    }
    if (!flag)
    {
        cout << "will take number" << '\n';
    } else {
        cout <<"will not take number" << '\n';
    }
    return 0;
}