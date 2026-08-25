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
void sortt(Node* head) {
    Node* i = head;
    for(Node* i = head; i!=nullptr; i=i->next) {
        for(Node* j = head; j->next!= nullptr; j = j->next) {
            if(j->val > j->next->val) {
                swap(j->val, j->next->val);
            }
        }
    }
}
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
        if(head ==nullptr) {
            head = n;
            tail = n;
        } else {
            tail ->next = n;
            n->prev = tail;
            tail = n;
        } 
    }
    sortt(head);
    Node* temp = head;
    while(temp != nullptr) {
        cout << temp->val << ' ';
        temp = temp->next;
    }
    cout << endl;
    return 0;
}