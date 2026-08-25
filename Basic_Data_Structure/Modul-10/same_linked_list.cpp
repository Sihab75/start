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
    Node* head1 = nullptr;
    Node* tail1 = nullptr;
    while(true) {
        int val;
        cin >> val;
        if(val==-1) {
            break;
        }
        Node* n = new Node(val);
        if(head1 == nullptr) {
            head1 = n;
            tail1 = n;
        } else {
            tail1->next = n;
            n->prev = tail1;
            tail1 = n;
        }
    }
    Node* head2 = nullptr;
    Node* tail2 = nullptr;
    while(true) {
        int val;
        cin >> val;
        if(val==-1) {
            break;
        }
        Node* n = new Node(val);
        if(head2==nullptr) {
            head2 = n;
            tail2 = n;
        } else {
            tail2->next = n;
            n->prev = tail2;
            tail2 = n;
        }
    }
    Node* temp1 = head1;
    Node* temp2 = head2;
    bool flag = true;
    while(temp1!=nullptr && temp2!=nullptr) {
        if(temp1->val != temp2->val) {
            flag = false;
            break;
        }
        temp1 = temp1->next;
        temp2 = temp2->next;
    }
    if(flag && (temp1 != nullptr || temp2 !=nullptr)) {
        flag = false;
    }
    cout << (flag? "Yes" : "NO") << endl;
    return 0;
}