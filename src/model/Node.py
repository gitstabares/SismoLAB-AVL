import graphviz
import copy

class Node:
    def __init__(self, value, parent = None):
        self.value = value
        self.parent = parent
        self.left_child = None
        self.right_child = None

    def __repr__(self):
        return str(self.value)

    def get_root(self):
        if not self.parent:
            return self
        return self.parent.get_root()

    def add_node(self, value):
        if self.value > value:
            if self.left_child == None:
                self.left_child = Node(value, self)
            else:
                self.left_child.add_node(value)
        elif self.value < value:
            if self.right_child == None:
                self.right_child = Node(value, self)
            else:
                self.right_child.add_node(value)

    def add_nodes(self, values):
        for value in values:
            self.add_node(value)

    def get_tree_graph(self):
        tree = graphviz.Digraph()
        self.__build_tree_graph(tree)
        return tree

    def __build_tree_graph(self,tree):
        tree.node(f"{self.value}")
        if self.left_child:
            self.left_child.__build_tree_graph(tree)
            tree.edge(f"{self.value}",f"{self.left_child.value}",label="L")
        if self.right_child:
            self.right_child.__build_tree_graph(tree)
            tree.edge(f"{self.value}",f"{self.right_child.value}",label="R")

    def get_node(self,value):
        if value == self.value:
            return self
        elif value > self.value and self.right_child:
            return self.right_child.get_node(value)
        elif value < self.value and self.left_child:
            return self.left_child.get_node(value)

    def copy_subtree(self,value):
        if value == self.value:
            self = copy.deepcopy(self)
            self.parent = None
            return self
        elif value > self.value and self.right_child:
            return self.right_child.copy_subtree(value)
        elif value < self.value and self.left_child:
            return self.left_child.copy_subtree(value)

    def get_weight(self):
        self.__weight = 1
        if self.left_child:
            self.__weight += self.left_child.get_weight()
        if self.right_child:
            self.__weight += self.right_child.get_weight()
        return self.__weight

    def get_deep(self):
        if self.parent:
            return self.parent.get_deep()+1
        return 0;

    def get_biggest(self):
        if self.right_child:
            return self.right_child.get_biggest()
        return self

    def get_smallest(self):
        if self.left_child:
            return self.left_child.get_smallest()
        return self

    def pop_node(self,value):
        node = self.get_node(value)
        if node:
            node.__delete_self()

    def pop_nodes(self,values):
        for value in values:
            self.pop_node(value)

    def __delete_self(self):
        if not (self.left_child and self.right_child):
            child = None
            if self.left_child:
                self.left_child.parent = self.parent
                child = self.left_child
            if self.right_child:
                self.right_child.parent = self.parent
                child = self.right_child
            if self.parent:
                if self.parent.value > self.value:
                    self.parent.left_child = child
                elif self.parent.value < self.value:
                    self.parent.right_child = child
            else:
                self.__dict__.update(child.__dict__)
        else:
            predecessor = self.left_child.get_biggest()
            value = predecessor.value
            predecessor.__delete_self()
            self.value = value

    def preorder_traversal(self, lista = []):
        lista.append(self.value)
        if self.left_child:
            lista = self.left_child.recorrido_preorden(lista)
        if self.right_child:
            lista = self.right_child.recorrido_preorden(lista)
        return lista

    def inorder_traversal(self, lista = []):
        if self.left_child:
            lista = self.left_child.recorrido_inorden(lista)
        lista.append(self.value)
        if self.right_child:
            lista = self.right_child.recorrido_inorden(lista)
        return lista

    def postorder_traversal(self, lista = []):
        if self.left_child:
            lista = self.left_child.recorrido_posorden(lista)
        if self.right_child:
            lista = self.right_child.recorrido_posorden(lista)
        lista.append(self.value)
        return lista

    def get_level_order_traversal(self):
        lista = [self]
        for i in lista:
            if i.left_child:
                lista.append(i.left_child)
            if i.right_child:
                lista.append(i.right_child)
        return lista

    def get_height(self):
        if self.left_child and self.right_child:
            return max(self.left_child.get_height(),self.right_child.get_height())+1 
        elif self.left_child:
            return self.left_child.get_height()+1
        elif self.right_child:
            return self.right_child.get_height()+1
        else:
            return 0

    def __get_balance_factor(self):
        return self.left_child.get_height()-self.right_child.get_height()

    def __rotate_left(self):
        if not self.right_child:
            return
        self.left_child = copy.deepcopy(self)
        self.left_child.parent = self
        self.left_child.right_child = self.right_child.left_child if self.right_child.left_child else None
        self.value = self.right_child.value
        self.right_child = self.right_child.right_child

    def __rotate_right(self):
        if not self.left_child:
            return
        self.right_child = copy.deepcopy(self)
        self.right_child.parent = self
        self.right_child.left_child = self.left_child.right_child if self.left_child.right_child else None
        self.value = self.right_child.value
        self.right_child = self.right_child.right_child

    def __balance_node(self):
        if self.__get_balance_factor() > 1:
            self.__rotate_right()
        elif self.__get_balance_factor() < -1:
            self.__rotate_left()