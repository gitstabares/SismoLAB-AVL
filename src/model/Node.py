# Base class for node
class Node:
    def __init__(self, key, parent = None):
        self.__key = key
        self.__left = None
        self.__right = None
        self.__parent = parent

    # Dunder method for representing a node
    def __repr__(self):
        return str(self.__key)

    # Getters and setters
    def get_key(self):
        return self.__key

    def set_key(self, key):
        self.__key = key

    def get_left(self):
        return self.__left

    def set_left(self, node):
        self.__left = node

    def get_right(self):
        return self.__right

    def set_right(self, node):
        self.__right = node

    def get_parent(self):
        return self.__parent

    def set_parent(self, node):
        self.__parent = node

    # Recursive funcion to get the certain node's height    
    def get_height(self):
        if self.__left and self.__right:
            # If the node has two children, gets the maximum height and adds one
            return max(self.__left.get_height(),self.__right.get_height())+1 
        # If it has only one child, adds one to the child's height
        elif self.__left:
            return self.__left.get_height()+1
        elif self.__right:
            return self.__right.get_height()+1
        else:
            return 0

    # Recursively gets the depth of a node
    def get_depth(self):
        if self.get_parent():
            # The depth of a node is its parent's depth plus one
            return self.get_parent().get_depth()+1
        return 0

    # Recursively gets the weight of a node
    def get_weight(self):
        # Start with a weight of one to account for the node itself
        weight = 1
        # If it has children, add each child's weight to its own
        if self.__left:
            weight += self.__left.get_weight()
        if self.__right:
            weight += self.__right.get_weight()
        return weight

    # Gets the balance factor as the difference between the heights of the left and right children
    def get_balance_factor(self):
        left_height = self.__left.get_height()+1 if self.__left else 0
        right_height = self.__right.get_height()+1 if self.__right else 0
        return left_height - right_height