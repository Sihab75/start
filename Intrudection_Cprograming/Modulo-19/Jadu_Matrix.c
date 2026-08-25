#include <stdio.h>
int main () {
    int row, col;
    scanf("%d %d", &row, &col);
    int mat[row][col];
    for(int i = 0; i < row;i++) {
        for(int j = 0; j < col; j++) {
            scanf("%d", &mat[i][j]);
        }
    }

    int isJadu = 1;
    if (row != col) {
       isJadu = 0;
    }
    for(int i = 0; i < row;i++) {
        for(int j = 0; j < col; j++) {
            if ((mat[i][j] !=1 && j==i) || (mat[i][j] != 0 && i!=j && i+j != row-1) || (mat[i][j]!=1 && ((i+j )== row-1))) {
                isJadu = 0;
                break;
            }
        }
    }
    
    if(isJadu==1){
        printf("YES\n");
    } 
    else {
        printf("NO\n");
    }
    return 0;
}