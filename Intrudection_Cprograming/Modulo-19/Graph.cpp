#include <bits/stdc++.h>
using namespace std;

int main () {
    int v, e;
    cin>> v >> e;
    vector<vector<int>> g(v);

    for (int i = 0; i < e;++i) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    
    
    return 0; 
}