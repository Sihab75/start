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
    if (head == nullptr) {
        head = newNode;
        tail = newNode;
        return;
    }
    tail->next = newNode;
    tail = tail->next;
}
void travers(Node* &head) {
    Node* temp = head;
    int mn = INT_MAX;
    int mx = INT_MIN;
    while(temp!=nullptr) {
        mn = min(mn, temp->val);
        mx = max(mx, temp->val);
        temp = temp->next;
    }
    cout << mx-mn << '\n';
}
int main () {
    Node* head = nullptr;
    Node* tail = nullptr;
    while (1) {
        int val;
        cin >> val;
        if (val == -1) {
            break;
        }
        insertAtTail(head, tail, val);
    }
    travers(head);
    return 0;
}