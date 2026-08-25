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
void printL (Node* temp) {
    while(temp!=nullptr) {
        cout<< temp->val << ' ';
        temp = temp->next;
    }
}
void printR(Node* temp) {
    while(temp!=nullptr) {
        cout<< temp->val << ' ';
        temp = temp->prev;
    }
}
int main () {
    Node* head = nullptr;
    Node* tail = nullptr;
    int size = 0;
    int q; 
    cin >> q;
    while(q--) {
        int x, val;
        cin >> x >> val;
        if (x<0 || size < x) {
            cout << "Invalid" << '\n';
            continue;
        }
        
        Node* n = new Node(val);
        
        if (x == 0) {
            if (head == nullptr) {
                head = tail = n;
            } else {
                n->next = head;
                head->prev = n;
                head = n;
            }
        } else if (x == size) {
            tail->next = n;
            n->prev = tail;
            tail = n;
        } else {
            Node* temp = head;
            int i = 0;
            while(i<x-1 && temp->next != nullptr) {
                temp = temp->next;
                i++;
            }
            n->next = temp->next;
            n->prev = temp;
            temp->next->prev = n;
            temp->next = n; 
        }
        size++;
        cout << "L -> ";
        printL(head);
        cout << '\n' << "R -> ";
        printR(tail);
        cout << '\n';
    }
    return 0;
}