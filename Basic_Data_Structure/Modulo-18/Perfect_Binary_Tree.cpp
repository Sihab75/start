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
int travers(Node* root) {
    if(root == nullptr) {
        return 0;
    }
    return 1+ max(travers(root->left),travers(root->right));
}
long long traversn(Node* root) {
    if(root == nullptr) {
        return 0;
    }
    return 1+ traversn(root->left)+ traversn(root->right);
}
int main () {
    Node* root = inputT();
    vector<int> a;
    int depth = travers(root);
    long long c = traversn(root);
    long long d = 1;
    while(depth--) {
        d*=2;
    }
    cout << ((c==d-1)?"YES":"NO") << '\n';
    return 0;
}