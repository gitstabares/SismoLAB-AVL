class Node:
    """Store a key and links to the node's children and parent."""

    def __init__(self, key):
        """Create a node with ``key`` and an optional parent.

        Args:
            key (Any): The key for the node.
            parent (Optional[Node]): The parent node, if any.
        """
        self.__key = key
        self.__left = None
        self.__right = None
        self.__parent = None

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, value: Node):
        self.__left = value

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, value: Node):
        self.__right = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value: Node):
        self.__parent = value

    def __repr__(self):
        """Return the string representation of this node's key.

        Returns:
            str: The string representation of the key.
        """
        return str(self.__key)

    def __eq__(self, other:Node):
        """Check if this node equals another based on key equality.

        Args:
            other (Any): Another node.

        Returns:
            bool: True if keys are equal, False otherwise.
        """
        return self.__key == other.key

    @property
    def height(self):
        """Return the height of this subtree (a leaf has height zero).

        Returns:
            int: The height of the subtree.
        """
        if self.left and self.right:
            return max(self.left.height, self.right.height) + 1 
        elif self.left:
            return self.left.height + 1
        elif self.right:
            return self.right.height + 1
        else:
            return 0

    @property
    def depth(self):
        """Return the number of parent links between this node and the root.

        Returns:
            int: The depth of the node.
        """
        return self.parent.depth + 1 if self.parent else 0

    @property
    def weight(self):
        """Return the number of nodes in this subtree, including this node.

        Returns:
            int: The weight (number of nodes).
        """
        weight = 1
        if self.left:
            weight += self.left.weight
        if self.right:
            weight += self.right.weight
        return weight

    @property
    def balance_factor(self):
        """Return left-subtree height minus right-subtree height.

        Returns:
            int: The balance factor.
        """
        left_height = self.left.height + 1 if self.left else 0
        right_height = self.right.height + 1 if self.right else 0
        return left_height - right_height

    @property
    def root(self):
        """Return the root node of the tree containing this node.

        Returns:
            Node: The root node.
        """
        return self if not self.parent else self.parent.root