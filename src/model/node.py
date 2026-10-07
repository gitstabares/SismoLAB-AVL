class Node:
    
    """Store a key and links to the node's children and parent."""

    def __init__(self, key):
        """Create a node with ``key`` and an optional parent.

        Args:
            key (Any): The key for the node.
            parent (Optional[Node]): The parent node, if any.
        """
        self._key = key
        self._left = None
        self._right = None
        self._parent = None

    def __repr__(self):
        """Return the string representation of this node's key.

        Returns:
            str: The string representation of the key.
        """
        return str(self.get_key())

    def __eq__(self, other: Node):
        """Check if this node equals another based on key equality.

        Args:
            other (Any): Another node.

        Returns:
            bool: True if keys are equal, False otherwise.
        """
        if not isinstance(other, Node):
            return False
        return self.get_key() == other.get_key()
    
    def get_key(self):
        return self._key

    def set_key(self, value):
        self._key = value

    def get_left(self) -> Node:
        return self._left

    def set_left(self, value: Node):
        self._left = value

    def get_right(self) -> Node:
        return self._right

    def set_right(self, value: Node):
        self._right = value

    def get_parent(self) -> Node:
        return self._parent

    def set_parent(self, value: Node):
        self._parent = value

    def get_height(self) -> int:
        """Return the height of this subtree (a leaf has height zero).

        Returns:
            int: The height of the subtree.
        """
        left = self.get_left()
        right = self.get_right()
        if left and right:
            return max(left.get_height(), right.get_height()) + 1
        elif left:
            return left.get_height() + 1
        elif right:
            return right.get_height() + 1
        else:
            return 0

    def get_depth(self) -> int:
        """Return the number of parent links between this node and the root.

        Returns:
            int: The depth of the node.
        """
        parent = self.get_parent()
        return parent.get_depth() + 1 if parent else 0

    def get_weight(self) -> int:
        """Return the number of nodes in this subtree, including this node.

        Returns:
            int: The weight (number of nodes).
        """
        weight = 1
        left = self.get_left()
        right = self.get_right()
        if left:
            weight += left.get_weight()
        if right:
            weight += right.get_weight()
        return weight

    def get_balance_factor(self) -> int:
        """Return left-subtree height minus right-subtree height.

        Returns:
            int: The balance factor.
        """
        left = self.get_left()
        right = self.get_right()
        left_height = left.get_height() + 1 if left else 0
        right_height = right.get_height() + 1 if right else 0
        return left_height - right_height

    def get_root(self) -> Node:
        """Return the root node of the tree containing this node.

        Returns:
            Node: The root node.
        """
        parent = self.get_parent()
        return self if not parent else parent.get_root()