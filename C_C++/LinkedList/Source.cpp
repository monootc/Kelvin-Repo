#include<iostream>

using namespace std;

struct Node{
	int data;
	Node *next;
	Node(int d, Node *n = NULL){
		data = d;
		next = n;
	}
};

class LinkedList{
private:
	Node* head;
	
public:
	LinkedList();
	void append(int data);
	void prepend(int data);
	void insert_node(int data, int position);
	void delete_node_by_data(int data);
	void delete_node_by_position(int position);
	int getLength();
	void print_list();
};

LinkedList::LinkedList(){
	head = NULL;
}

void LinkedList::append(int data){
	if (head == NULL){
		head = new Node(data);
	}
	else{
		Node *cur = head;
		while (cur->next != NULL){
			cur = cur->next;
		}
		cur->next = new Node(data);
	}	
}

void LinkedList::prepend(int data){
	if (head == NULL){
		head = new Node(data);
	}
	else{
		Node *newHead = new Node(data, head);
		head = newHead;
	}
}

int LinkedList::getLength(){
	if (head == NULL){
		return 0;
	}
	else{
		int count = 0;
		Node *cur = head;
		while (cur != NULL){
			cur = cur->next;
			count++;
		}
		return count;
	}
}

void LinkedList::insert_node(int data, int position){
	if (head == NULL){
		if (position == 0){
			head = new Node(data);
		}
		else{
			cout << "cannot insert data at position " << position << ", list is empty" << endl;
			return;
		}
	}
	else if (position > getLength()){
		cout << "cannot insert data at postion " << position << endl;
		return;
	}
	else{
		Node *cur = head;
		Node *prev = head;
		for (int i = 0; i < position; i++){
			prev = cur;
			cur = cur->next;
		}
		Node *newNode = new Node(data, cur);
		prev->next = newNode;
	}
}

void LinkedList::delete_node_by_data(int data){
	if (head == NULL){
		cout << "Empty list" << endl;
		return;
	}
	else if (head->data == data){
		head = head->next;
	}
	else{
		Node *cur = head;
		Node *prev = head;
		bool found = false;
		while (cur != NULL){
			if (cur->data == data){
				found = true;
				break;
			}
			prev = cur;
			cur = cur->next;
		}

		if (!found){
			cout << "value " << data << " is not in the list" << endl;
		}
		else{
			prev->next = cur->next;
		}
	}
}

void LinkedList::delete_node_by_position(int position){
	if (head == NULL){
		cout << "Empty list" << endl;
		return;
	}
	else if (position > getLength()){
		cout << "position " << position << " is greater than the length of the list" << endl;
		return;
	}
	else if (position == 0){
		head = head->next;
	}
	else{
		Node *cur = head;
		Node *prev = head;
		for (int i = 0; i < getLength(); i++){
			prev = cur;
			cur = cur->next;
		}
		prev->next = cur->next;
	}
}

void LinkedList::print_list(){
	if (head == NULL){
		cout << "Empty list" << endl;
		return;
	}
	else{
		Node *cur = head;
		while (cur != NULL){
			cout << cur->data << " ";
			cur = cur->next;
		}
		cout << endl;
	}
}


int main(){
	LinkedList l1;
	l1.append(5);
	l1.append(15);
	l1.append(51);
	l1.prepend(10);
	l1.insert_node(1, 1);
	l1.delete_node_by_data(11);
	l1.delete_node_by_position(0);
	l1.print_list();

	system("pause");
}