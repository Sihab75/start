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
        head=newNode;
        tail= newNode;
        return;
    }
    tail->next = newNode;
    tail = tail->next;
}
void insertAtHead(Node* &head, Node* &tail, int val) {
    Node* newNode=new Node(val);
    if(head==nullptr) {
        head = newNode;
        tail = newNode;
        return;
    }
    newNode->next = head;
    head = newNode;
}
void deleteAtAnyPosition(Node* &head, Node* &tail, int pos) {
    if(head==nullptr) {
        return;
    }
    Node* deleteNode = nullptr;
    if(pos == 0) {
        deleteNode = head;
        head = head->next;
        if(head == nullptr) {
            tail = nullptr;
        }
        delete deleteNode;
        return;
    }
    int idx = 0; 
    Node* temp = head;
    Node* prev = nullptr;
    while(temp!=nullptr && idx<pos) {
        prev = temp;
        temp=temp->next;
        idx++;
    }
    if(temp==nullptr) {
        return;
    }
    if (temp->next == nullptr) {
        deleteNode = temp;
        temp = prev;
        temp->next = nullptr;
        tail = temp;
        delete deleteNode;
        return;
    }
    deleteNode = temp;
    prev->next = temp->next;
    temp = prev;
    delete deleteNode;
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
    int t;
    cin >> t;
    while(t--) {
        int x, val;
        cin >> x >> val;
        if (x==0) {
            insertAtHead(head, tail, val);
        } else if (x==1) {
            insertAtTail(head, tail, val);
        } else if(x==2) {
            deleteAtAnyPosition(head, tail, val);
        }
        print(head);
    }
    return 0;
}