#include<bits/stdc++.h>
using namespace std;

class Node{
public:
    int val;
    Node* next;
    Node* prev;
    Node(int val) {
        this->val = val;
        next = nullptr;
        prev = nullptr;
    }
};

int main () {
    Node* head = nullptr;
    Node* tail = nullptr;
    while (true) {
        int val;
        cin >> val;
        if(val==-1) {
            break;
        }
        Node* n = new Node(val);
        if(head == nullptr) {
            head = n;
            tail = n;
        } else {
            tail->next = n;
            n->prev = tail;
            tail = n;
        }
    }
    Node* i = head;
    Node* j = tail;
    while(i!=j && i->prev !=j) {
        swap(i->val, j->val);
        i=i->next;
        j = j->prev;
    }
    Node* temp = head;
    while(temp!=nullptr) {
        cout << temp->val << ' ';
        temp = temp->next;
    }
    return 0;
}