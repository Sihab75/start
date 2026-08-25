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
        tail= newNode;
    }
    tail->next = newNode;
    tail = tail->next;
}

void travers(Node* &head1, Node* &head2) {
    Node* temp1 = head1;
    Node* temp2 = head2;
    int flag = 1;
    while(temp1!=nullptr && temp2!=nullptr) {
        if(temp1->val != temp2->val) {
            flag = 0;
            break;
        }
        temp1 = temp1->next;
        temp2=temp2->next;
    }
    if (flag==0) {
        cout << "NO" << '\n';
    } else if(temp1!=nullptr|| temp2!=nullptr) {
        cout << "NO" << '\n';
    } else {
        cout << (flag==1?"YES":"NO") << '\n';
    }
}

int main () {
    Node* head1 = nullptr;
    Node* tail1 = nullptr;
    Node* head2 = nullptr;
    Node* tail2 = nullptr;
    while (1) {
        int val;
        cin >> val;
        if(val == -1) {
            break;
        }
        insertAtTail(head1, tail1, val);
    }
    while (1) {
        int val;
        cin >> val;
        if (val==-1) {
            break;
        }
        insertAtTail(head2, tail2, val);
    }
    travers(head1, head2);
    return 0;
}