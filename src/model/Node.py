import graphviz
import copy

class Node:
    # Constructor
    def __init__(self, key, parent = None):
        self.key = key
        self.parent = parent
        self.left_child = None
        self.right_child = None

    # Dunder function to print the node's key
    def __repr__(self):
        return str(self.key)

    # Function to get the root from any node in the tree
    def get_root(self):
        if not self.parent:
            return self
        return self.parent.get_root()

    # Function to add a single node
    def add_node(self, key):
        if self.key > key:
            if self.left_child == None:
                self.left_child = Node(key, self)
            else:
                self.left_child.add_node(key)
        elif self.key < key:
            if self.right_child == None:
                self.right_child = Node(key, self)
            else:
                self.right_child.add_node(key)
        # The case of the node in the tree is not considered yet

    # Function to add multiple nodes
    def add_nodes(self, keys):
        for key in keys:
            self.add_node(key)

    # Construction of tree Dot object to graphviz
    def get_tree_graph(self):
        tree = graphviz.Digraph()
        self.__build_tree_graph(tree)
        return tree

    # Recursive construction of tree
    def __build_tree_graph(self,tree):
        tree.node(f"{self.key}")
        if self.left_child:
            tree.edge(f"{self.key}",f"{self.left_child.key}",label="L")
            self.left_child.__build_tree_graph(tree)
        if self.right_child:
            tree.edge(f"{self.key}",f"{self.right_child.key}",label="R")
            self.right_child.__build_tree_graph(tree)

    # Searching function to look for a specific node
    def get_node(self,key):
        if key == self.key:
            return self
        elif key > self.key and self.right_child:
            return self.right_child.get_node(key)
        elif key < self.key and self.left_child:
            return self.left_child.get_node(key)

    # Copy function to avoid reference mistakes
    def copy(self):
        new_copy = self.__copy()
        new_copy.parent = None
        return new_copy

    # Recursive function to copy subtree
    def __copy(self):
        new_copy = copy.copy(self)
        if new_copy.left_child:
            new_copy.left_child = new_copy.left_child.__copy()
            new_copy.left_child.parent = new_copy
        if new_copy.right_child:
            new_copy.right_child = new_copy.right_child.__copy()
            new_copy.right_child.parent = new_copy
        return new_copy

    # Count function to get the subtree's weight
    def get_weight(self):
        self.__weight = 1
        if self.left_child:
            self.__weight += self.left_child.get_weight()
        if self.right_child:
            self.__weight += self.right_child.get_weight()
        return self.__weight

    # Recursive function to get the distance from node to root
    def get_deep(self):
        if self.parent:
            return self.parent.get_deep()+1
        return 0;

    # Recursive function to get the distance from node to farest leaf node
    def get_height(self):
        if self.left_child and self.right_child:
            return max(self.left_child.get_height(),self.right_child.get_height())+1 
        elif self.left_child:
            return self.left_child.get_height()+1
        elif self.right_child:
            return self.right_child.get_height()+1
        else:
            return 0

    # Get the rightmost node
    def get_biggest(self):
        if self.right_child:
            return self.right_child.get_biggest()
        return self

    # Get the leftmost node
    def get_smallest(self):
        if self.left_child:
            return self.left_child.get_smallest()
        return self

    # Delete a single node 
    def pop_node(self,key):
        node = self.get_node(key)
        if node:
            node.__delete_self()

    # Delete multiple nodes
    def pop_nodes(self,keys):
        for key in keys:
            self.pop_node(key)

    # Delete itself
    def __delete_self(self):
        # If node has one or zero children
        if not (self.left_child and self.right_child):
            child = None
            # Updating parent reference in child
            if self.left_child:
                self.left_child.parent = self.parent
                child = self.left_child
            if self.right_child:
                self.right_child.parent = self.parent
                child = self.right_child
            # Updating child reference in parent
            if self.parent:
                if self.parent.key > self.key:
                    self.parent.left_child = child
                elif self.parent.key < self.key:
                    self.parent.right_child = child
            else:
                self.__dict__.update(child.__dict__)
        # Using predecessor in case node has two children
        else:
            predecessor = self.left_child.get_biggest()
            key = predecessor.key
            predecessor.__delete_self()
            self.key = key

    # Traversals
    def preorder_traversal(self, lista = []):
        lista.append(self)
        if self.left_child:
            lista = self.left_child.preorder_traversal(lista)
        if self.right_child:
            lista = self.right_child.preorder_traversal(lista)
        return lista

    def inorder_traversal(self, lista = []):
        if self.left_child:
            lista = self.left_child.inorder_traversal(lista)
        lista.append(self)
        if self.right_child:
            lista = self.right_child.inorder_traversal(lista)
        return lista

    def postorder_traversal(self, lista = []):
        if self.left_child:
            lista = self.left_child.postorder_traversal(lista)
        if self.right_child:
            lista = self.right_child.postorder_traversal(lista)
        lista.append(self)
        return lista

    def get_level_order_traversal(self):
        queue = [self]
        for node in queue:
            if node.left_child:
                queue.append(node.left_child)
            if node.right_child:
                queue.append(node.right_child)
        return queue

    # Balance factor from difference between height in children
    def __get_balance_factor(self):
        left_height = self.left_child.get_height()+1 if self.left_child else 0
        right_height = self.right_child.get_height()+1 if self.right_child else 0
        return left_height - right_height

    # Simple rotation to left
    def __rotate_left(self):
        self.left_child = copy.copy(self)
        self.left_child.parent = self
        self.left_child.right_child = self.right_child.left_child
        self.key = self.right_child.key
        self.right_child = self.right_child.right_child

    # Simple rotation to right
    def __rotate_right(self):
        self.right_child = copy.copy(self)
        self.right_child.parent = self
        self.right_child.left_child = self.left_child.right_child
        self.key = self.left_child.key
        self.left_child = self.left_child.left_child

    # Balancing cases for a node
    def __balance_node(self):
        while self.__get_balance_factor() > 1:
            if self.left_child.__get_balance_factor() < 0:
                self.left_child.__rotate_left()
            self.__rotate_right()
        while self.__get_balance_factor() < -1:
            if self.right_child.__get_balance_factor() > 0:
                self.right_child.__rotate_right()
            self.__rotate_left()

    def is_balanced(self):
        for node in self.get_level_order_traversal():
            if abs(node.__get_balance_factor()) > 1:
                return False
        return True

    def balance_tree(self):
        while not self.is_balanced():
            for node in reversed(self.get_level_order_traversal()):
                node.__balance_node()

    def balance_branch(self):
        self.__balance_node()
        if self.parent:
            self.parent.balance_branch()