#include<bits/stdc++.h>
using namespace std;
vector<int> vis(1e4+7,0);
class Node{
public:
    int val;
    Node* next;
    Node(int val) {
        this->val = val;
        next = nullptr;
    }
};
void insertAtTail(Node* &head, Node* &tail, int val) {
    if(vis[val] == 1) {
        return;
    }
    Node* newNode=new Node(val);
    vis[val] = 1;
    if(head==nullptr) {
        head = newNode;
        tail = newNode;
        return;
    }
    tail->next = newNode;
    tail = tail->next;
}
void print(Node* &head) {
    Node* temp = head;
    while(temp!=nullptr) {
        cout << temp->val << ' ';
        temp=temp->next;
    }
    cout << '\n';
}
int main () {
    Node* head = nullptr;
    Node* tail = nullptr;
    while(1) {
        int val;
        cin >> val;
        if(val==-1) {
            break;
        }
        insertAtTail(head, tail, val);
    }
    print(head);
    return 0;
}