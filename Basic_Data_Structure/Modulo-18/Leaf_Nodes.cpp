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
void travers(Node* root, vector<int> &ans) {
    if(root == nullptr){
        return;
    }
    if(root->left == nullptr && root->right==nullptr) {
        ans.push_back(root->val);
    }
    travers(root->left, ans);
    travers(root->right, ans);
}
bool cmp (int val1, int val2){
    return val1>val2;
}
int main () {
    Node* root = inputT();
    vector<int> ans;
    travers(root, ans);
    sort(ans.begin(), ans.end(), cmp);
    for(auto val: ans){
        cout << val << ' ';
    }
    cout << '\n';
    return 0;
}