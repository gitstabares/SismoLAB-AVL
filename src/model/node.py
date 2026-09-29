"""Define a node used to build a binary tree."""


class Node:
    """Store a key and links to the node's children and parent."""

    def __init__(self, key, parent = None):
        """Create a node with ``key`` and an optional parent."""
        self.__key = key
        self.__left = None
        self.__right = None
        self.__parent = parent

    def __repr__(self):
        """Return the string representation of this node's key."""
        return str(self.__key)

    def get_key(self):
        """Return this node's key."""
        return self.__key

    def set_key(self, key):
        """Replace this node's key with ``key``."""
        self.__key = key

    def get_left(self):
        """Return the left child, or ``None`` if absent."""
        return self.__left

    def set_left(self, node):
        """Set the left child to ``node``."""
        self.__left = node

    def get_right(self):
        """Return the right child, or ``None`` if absent."""
        return self.__right

    def set_right(self, node):
        """Set the right child to ``node``."""
        self.__right = node

    def get_parent(self):
        """Return the parent, or ``None`` if this is a root node."""
        return self.__parent

    def set_parent(self, node):
        """Set the parent node to ``node``."""
        self.__parent = node

    def get_height(self):
        """Return the height of this subtree (a leaf has height zero)."""
        if self.__left and self.__right:
            return max(self.__left.get_height(),self.__right.get_height())+1 
        elif self.__left:
            return self.__left.get_height()+1
        elif self.__right:
            return self.__right.get_height()+1
        else:
            return 0

    def get_depth(self):
        """Return the number of parent links between this node and the root."""
        return self.__parent.get_depth()+1 if self.__parent else 0

    def get_weight(self):
        """Return the number of nodes in this subtree, including this node."""
        weight = 1
        if self.__left:
            weight += self.__left.get_weight()
        if self.__right:
            weight += self.__right.get_weight()
        return weight

    def get_balance_factor(self):
        """Return left-subtree height minus right-subtree height."""
        left_height = self.__left.get_height()+1 if self.__left else 0
        right_height = self.__right.get_height()+1 if self.__right else 0
        return left_height - right_height

    def get_root(self):
        """Return the root node of the tree containing this node."""
        return self if not self.__parent else self.__parent.get_root()