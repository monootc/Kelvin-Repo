#include <iostream>

using namespace std;

class Node{
private:
	int data;
	Node *left;
	Node *right;
public:
	Node(int d, Node *l = NULL, Node *r=NULL) :
		data(d), left(l), right(r) {}
	void setData(int d);
	void setLeft(Node *node);
	void setRight(Node *node);
	int getData();
	Node* getLeft();
	Node* getRight();
};

int Node::getData(){
	return data;
}

Node* Node::getLeft(){
	return left;
}

Node* Node::getRight(){
	return right;
}

void Node::setData(int d){
	data = d;
}

void Node::setLeft(Node* l){
	left = l;
}

void Node::setRight(Node* r){
	right = r;
}



class BinaryTree{
public:
	BinaryTree();
	~BinaryTree();
	void insert(int data);
	void inorder_print();
	void preorder_print();
	int maxDepth();
	bool search(int data);
	
private:
	Node *root;
	void insert(Node *node, int data);
	void inorder_print(Node *node);
	void preorder_print(Node *node);
	int maxDepth(Node *node);
	bool search(Node *node, int data);
	void destroyTree(Node *node);
};

BinaryTree::BinaryTree(){
	root = NULL;
}

BinaryTree::~BinaryTree(){
	destroyTree(root);
}


void BinaryTree::insert(Node *node, int data){
	if (data < node->getData()){
		if (node->getLeft() == NULL){
			node->setLeft(new Node(data));
		}
		else{
			insert(node->getLeft(), data);
		}
	}
	else{
		if (node->getRight() == NULL){
			node->setRight(new Node(data));
		}
		else{
			insert(node->getRight(), data);
		}
	}
}

void BinaryTree::insert(int data){
	if (root == NULL){
		root = new Node(data);
	}
	else{
		insert(root, data);
	}
}

void BinaryTree::preorder_print(Node* node){
	if (node != NULL){
		cout << node->getData() << endl;
		preorder_print(node->getLeft());
		preorder_print(node->getRight());
	}
}

void BinaryTree::preorder_print(){
	preorder_print(root);
}

void BinaryTree::inorder_print(Node* node){
	if (node != NULL){
		inorder_print(node->getLeft());
		cout << node->getData() << endl;
		inorder_print(node->getRight());
	}
}

void BinaryTree::inorder_print(){
	inorder_print(root);
}

int BinaryTree::maxDepth(Node* node){
	int l = 0;
	int r = 0;
	if (node->getLeft() != NULL){
		l = maxDepth(node->getLeft()) + 1;
	}
	if (node->getRight() != NULL){
		r = maxDepth(node->getRight()) + 1;
	}
	return (l > r) ? l : r;
}

int BinaryTree::maxDepth(){
	if (root == NULL){
		return 0;
	}
	else if (root->getLeft() == NULL && root->getRight() == NULL){
		return 1;
	}
	else{
		maxDepth(root);
	}
}

bool BinaryTree::search(Node* node, int data){
	if (node != NULL){
		if (node->getData() == data){
			return true;
		}
		else if (node->getData() > data){
			return search(node->getLeft(), data);
		}
		else{
			return search(node->getRight(), data);
		}
	}
	else{
		return false;
	}
}

bool BinaryTree::search(int data){
	return search(root, data);
}

void BinaryTree::destroyTree(Node* node){
	if (node != NULL){
		destroyTree(node->getLeft());
		destroyTree(node->getRight());
		delete node;
	}
}


int main(){
	BinaryTree b;
	b.insert(10);
	b.insert(11);
	b.insert(19);
	b.insert(9);
	b.insert(5);
	b.insert(1);
	b.insert(210);
	b.inorder_print();
	cout << "is 10 in tree? " << b.search(10) << endl;
	system("pause");
}