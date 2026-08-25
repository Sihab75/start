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

void reversLinkedList(Node* &head, Node* &tail, Node* temp) {
    if (temp->next == nullptr) {
        head = temp;
        return;
    }
    reversLinkedList(head, tail, temp->next);
    temp->next->next = temp;
    temp->next = nullptr;
    tail = temp;
}

int main () {
    int n ;
    cin >> n;
    Node* head = nullptr;
    Node* tail = nullptr;
    for (int i = 0; i < n;i++) {
        int val;
        cin >> val;
        Node* n = new Node(val);
        if (head==nullptr) {
            head = n;
            tail = n;
        } else {
            tail->next = n;
            tail = n;
        }
    }
    Node* temp = head;
    while(temp!=nullptr) {
        cout << temp->val << ' ';
        temp=temp->next;
    }
    cout << endl;
    reversLinkedList(head, tail, head);
    temp = head;
    while(temp!=nullptr) {
        cout << temp->val << ' ';
        temp=temp->next;
    }
    cout << endl;
    return 0;
}