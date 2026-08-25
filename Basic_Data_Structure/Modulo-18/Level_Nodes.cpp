#include<bits/stdc++.h>
using namespace std;
class Node{
public:
    int val;
    Node* left;
    Node* right;
    Node(int val) {
        this->val = val;
        left = nullptr;
        right = nullptr;
    }
};

Node* inputT() {
    queue<Node*> q;
    int val;
    cin >> val;
    if(val==-1) return nullptr;
    Node* root = new Node(val);
    q.push(root);
    
    while(!q.empty()) {
        Node* myn = q.front();
        q.pop();
        int l, r;
        cin >> l >> r;
        if(l!=-1) {
            myn->left = new Node(l);
            q.push(myn->left);
        } 
        if(r!=-1) {
            myn->right=new Node(r);
            q.push(myn->right);
        }
    }
    return root;
}
void travers(Node* root, int level, vector<int> &a, int x) {
    if(root==nullptr) {
        return;
    }
    if(level == x) {
        a.push_back(root->val);
    }
    travers(root->left, level+1, a, x);
    travers(root->right, level+1, a, x);
}
int main () {
    Node* root = inputT();
    vector<int> a;
    int x;
    cin >> x;
    travers(root, 0, a, x);
    for(auto val: a) {
        cout << val << ' ';
    }
    cout  << (a.empty()? "Invalid": "")<< '\n';
    return 0;
}