import graphviz
import copy

class Node:
    # Constructor
    def __init__(self, key, parent = None):
        self.__key = key
        self.__parent = parent
        self.__left_child = None
        self.__right_child = None

    # Getters
    @property
    def key(self):
        return self.__key

    @property
    def parent(self):
        return self.__parent

    @property
    def left_child(self):
        return self.__left_child

    @property
    def right_child(self):
        return self.__right_child

    # Setters
    @key.setter
    def key(self,key):
        self.__key = key

    @parent.setter
    def parent(self,parent):
        self.__parent = parent

    @left_child.setter
    def left_child(self,left_child):
        self.__left_child = left_child

    @right_child.setter
    def right_child(self,right_child):
        self.__right_child = right_child

    # Dunder function to print the node's key
    def __repr__(self):
        return str(self.key)

    # Function to get the root from any node in the tree
    def get_root(self):
        if not self.parent:
            return self
        return self.parent.get_root()

    # Function to add a single node
    def add_node(self, node):
        if self.key > node.key:
            if self.left_child == None:
                self.left_child = node
            else:
                self.left_child.add_node(node)
        elif self.key < node.key:
            if self.right_child == None:
                self.right_child = node
            else:
                self.right_child.add_node(node)

    # Function to add multiple nodes
    def add_nodes(self, keys):
        for key in keys:
            self.add_node(key)
            
    # Function to get the tree in JSON format
    def to_dict(self):
        result = {}
        for key,value in self.__dict__.items():
            key = key.split("__")[-1]
            if key == 'parent':
                continue
            if isinstance(value,Node):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

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

    # Copy function avoiding reference mistakes
    def copy_subtree(self):
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
            left_child = self.left_child
            right_child = self.right_child
            parent = self.parent
            predecessor = self.left_child.get_biggest()
            self.__dict__.update(predecessor.__dict__)
            self.left_child = left_child
            self.right_child = right_child
            self.parent = parent
            predecessor.__delete_self()

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
        left_child = copy.copy(self)
        left_child.parent = self
        left_child.right_child = self.right_child.left_child
        parent = self.parent
        self.__dict__.update(self.right_child.__dict__)
        self.parent = parent
        self.left_child = left_child

    # Simple rotation to right
    def __rotate_right(self):
        right_child = copy.copy(self)
        right_child.parent = self
        right_child.left_child = self.left_child.right_child
        parent = self.parent
        self.__dict__.update(self.left_child.__dict__)
        self.parent = parent
        self.right_child = right_child

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