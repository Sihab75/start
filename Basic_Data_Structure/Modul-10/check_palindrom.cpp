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
    while(true) {
        int val;
        cin >> val;
        if(val==-1) {
            break;
        }
        Node* n = new Node(val);
        if(head==nullptr) {
            head = n;
            tail = n;
        } else {
            tail->next = n;
            n->prev = tail;
            tail = n;
        }
    }
    Node* i = head;
    Node* j= tail;
    bool flag = true;
    while(i<j && i->prev !=j) {
        if(i->val != j->val) {
            flag = false;
            break;
        }
        i = i->next;
        j=j->next;
    }
    cout << (flag? "YES": "NO") << endl;
    return 0;
}