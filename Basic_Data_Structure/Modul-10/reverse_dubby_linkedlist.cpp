#include<bits/stdc++.h>
using namespace std;
class Node {
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
    int n;
    cin >> n;
    Node* head = nullptr;
    Node* tail = nullptr;
    for(int i = 0; i < n; i++) {
        int val;
        cin >> val;
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
    Node* temp = head;
    while(temp!=nullptr) {
        cout << temp->val << ' ';
        temp=temp->next;
    }
    cout << endl;
    Node* i = head;
    Node* j = tail;
    while(i!=j && j !=i->prev) {
        swap(i->val, j->val);
        i = i->next;
        j = j->prev;
    }
    temp = head;
    while(temp!=nullptr) {
        cout << temp->val << ' ';
        temp=temp->next;
    } 
    cout << endl;
    return 0;
}