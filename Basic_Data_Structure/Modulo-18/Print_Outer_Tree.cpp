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
void left(Node* root, vector<int> &a) {
    if(root == nullptr) {
        return;
    }
    if(!root->left && !root->right) {
        a.push_back(root->val);
        return;
    }
    if(root->left)left(root->left, a);
    else  left(root->right, a);
    a.push_back(root->val);
}
void right(Node* root, vector<int> &a) {
    if(root == nullptr) {
        return;
    }
    if(!root->left && !root->right) {
        a.push_back(root->val);
        return;
    }
    a.push_back(root->val);
    if(root->right) right(root->right, a);
    else right(root->left, a);
}
int main () {
    Node* root = inputT();
    if(!root) return 0;

    vector<int> a;
    if(!root->left && !root->right) {
        a.push_back(root->val);
    } else {
        if(root->left) left(root->left,a);
        a.push_back(root->val);
        if(root->right) right(root->right, a); 
    }
    
    for(auto val: a) {
        cout << val << ' ';
    }
    cout << '\n';
    return 0;
}