class Node:
    def __init__(self, key, parent = None):
        self.__key = key
        self.__left = None
        self.__right = None
        self.__parent = parent

    def __repr__(self):
        return str(self.__key)

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

    def get_height(self):
        if self.__left and self.__right:
            return max(self.__left.get_height(),self.__right.get_height())+1 
        elif self.__left:
            return self.__left.get_height()+1
        elif self.__right:
            return self.__right.get_height()+1
        else:
            return 0

    def get_depth(self):
        if self.get_parent():
            return self.get_parent().get_depth()+1
        return 0

    def get_balance_factor(self):
        left_height = self.__left.get_height()+1 if self.__left else 0
        right_height = self.__right.get_height()+1 if self.__right else 0
        return left_height - right_height