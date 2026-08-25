

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int N;
        long long K;
        cin >> N >> K;
        vector<long long> A(N);
        for (auto &x : A)
            cin >> x;
        for (int i = 0; i < N; i++) {
            int best = i;
            for (int j = i + 1; j < N; j++) {
                bool possible = true;
                for (int p = j; p > i; p--) {
                    if (A[j] + A[p - 1] > K) {
                        possible = false;
                        break;
                    }
                }
                if (possible && A[j] < A[best]) {
                    best = j;
                }
            }
            if (best != i) {
                long long x = A[best];
                for (int j = best; j > i; j--) {
                    A[j] = A[j - 1];
                }
                A[i] = x;
            }
        }
        for (auto x : A)
            cout << x << ' ';
        cout << '\n';
    }
    return 0;
}