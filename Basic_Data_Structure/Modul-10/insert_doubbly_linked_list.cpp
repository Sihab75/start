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
    int q;
    cin >> q;
    Node* head = nullptr;
    Node* tail = nullptr;
    while (q--) {
        int x, v;
        cin >> x >> v;
        Node* n = new Node(v);
        if (x == 0 && head == nullptr) {
            head = n;
            tail = n;
            
        } else if(x== 0) {
            n->next = head;
            head->prev = n;
            head = n;
            
        }else {
            Node* temp = head;
            int i = 0;
            while(i<x-1 && temp->next != nullptr) {
                temp = temp->next;
                i++;
            }
            if(i== x-1 && temp->next !=nullptr) {
                temp->next->prev = n;
                n->next = temp->next;
                temp->next = n;
                n->prev = temp;
            }
            else if(i==x-1 && temp!=nullptr) {
                temp->next = n;
                n->prev = temp;
                tail = n;
            } else {
                cout << "Invalid" << endl;
                delete n;
                continue;
            }
        }
        
        Node* temp = head;
        while(temp!=nullptr) {
            cout << temp->val << ' ';
            temp = temp->next;
        }
        cout<< endl;
        temp = tail;
        while(temp != nullptr) {
            cout << temp->val << ' ';
            temp = temp->prev;
        }
        cout << endl;
    }
    return 0;
}