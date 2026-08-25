#include<bits/stdc++.h>
using namespace std;

class Node{
public:
    string val;
    Node* next;
    Node* prev;

    Node(string val){
        this->val = val;
        next = nullptr;
        prev = nullptr;
    }
};

int main(){
    Node* head = nullptr;
    Node* tail = nullptr;
    string s;
    while(cin >> s && s != "end") {
        Node* n = new Node(s);
        if(head == nullptr){
            head = tail = n;
        }else{
            tail->next = n;
            n->prev = tail;
            tail = n;
        }
    }
    Node* current = head;
    int q;
    cin >> q;
    while(q--){
        string cmd;
        cin >> cmd;
        if(cmd == "visit"){
            string address;
            cin >> address;
            Node* temp = head;
            bool found = false;
            while(temp != nullptr){
                if(temp->val == address){
                    current = temp;
                    cout << current->val << '\n';
                    found = true;
                    break;
                }
                temp = temp->next;
            }
            if(!found){
                cout << "Not Available\n";
            }
        }else if(cmd == "next"){
            if(current->next != nullptr){
                current = current->next;
                cout << current->val << '\n';
            }
            else{
                cout << "Not Available\n";
            }
        }
        else if(cmd == "prev"){
            if(current->prev != nullptr){
                current = current->prev;
                cout << current->val << '\n';
            }
            else{
                cout << "Not Available\n";
            }
        }
    }
    return 0;
}