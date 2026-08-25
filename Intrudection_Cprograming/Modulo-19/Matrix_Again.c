#include <stdio.h>
int main () {
    int row, col;
    scanf("%d %d", &row, &col);
    int mat[row][col];
    for(int i = 0; i < row; i++) {
        for(int j = 0; j < col; j++) {
            scanf("%d", &mat[i][j]);
        }
    }
    for(int i = 0; i < col; i++) {
        printf("%d ", mat[row-1][i]);
    }
    printf("\n");
    for(int i = 0; i < row; i++) {
        printf("%d ", mat[i][col-1]);
    }
    printf("\n");
    return 0;
}