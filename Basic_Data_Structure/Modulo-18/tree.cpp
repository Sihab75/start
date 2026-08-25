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
void levelOrder(Node* root) {
    queue<Node*> q;
    q.push(root);
    while(!q.empty()) {
        Node* n = q.front();
        q.pop();
        cout << n->val << ' ';
        if(n->left) {
            q.push(n->left);
        }
        if(n->right) q.push(n->right);
    }
    cout << endl;
}
int main () {
    Node* root = inputT();
    levelOrder(root);
    return 0;
}