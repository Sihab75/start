#include<bits/stdc++.h>
using namespace std;
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
    Node* newNode = new Node(val);
    if (head==nullptr) {
        head = newNode;
        tail = newNode;
        return;
    }
    tail->next = newNode;
    tail = tail->next;
}
void travers(Node* &head, int val) {
    Node* temp = head;
    int idx = 0;
    int flag = 0;
    while(temp !=nullptr) {
        if (temp->val == val) {
            flag = 1;
            break;
        }
        temp = temp->next;
        idx++;
    }
    cout << (flag?idx:-1) << '\n';
}
int main () {
    int t;
    cin >> t;
    while(t--) {
        Node* head = nullptr;
        Node* tail = nullptr;
        while(1) {
            int val;
            cin >> val;
            if (val==-1) {
                break;
            }
            insertAtTail(head, tail, val);
        }
        int val;
        cin >> val;
        travers(head, val);
    }
    return 0;
}