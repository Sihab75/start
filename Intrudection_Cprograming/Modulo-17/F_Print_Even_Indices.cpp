#include <bits/stdc++.h>
using namespace std;

void printArray(int arr[], int n) {
    if(n<0) return;
    if (n==0){
        cout<<arr[n];
        return;
    } 
    if(n%2==0) {
        cout << arr[n] << ' ';
    }
    printArray(arr, --n);
} 

void arrayInput(int arr[], int n) {
    if(n<0) return;
    arrayInput (arr, n-1);
    cin>> arr[n];
}

int main () {
    int n;
    cin >> n;
    int arr[n];
    arrayInput(arr, n-1);
    printArray(arr, n-1);
    cout<<'\n';
}