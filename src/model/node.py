from typing import Any, Optional

class Node:
    """Store a key and links to the node's children and parent."""

    def __init__(self, key: Any, parent: Optional['Node'] = None) -> None:
        """Create a node with ``key`` and an optional parent.

        Args:
            key (Any): The key for the node.
            parent (Optional[Node]): The parent node, if any.
        """
        self.__key = key
        self.__left: Optional['Node'] = None
        self.__right: Optional['Node'] = None
        self.__parent: Optional['Node'] = parent

    def __repr__(self) -> str:
        """Return the string representation of this node's key.

        Returns:
            str: The string representation of the key.
        """
        return str(self.__key)

    def __eq__(self, other: Any) -> bool:
        """Check if this node equals another based on key equality.

        Args:
            other (Any): Another node.

        Returns:
            bool: True if keys are equal, False otherwise.
        """
        if not hasattr(other, 'get_key'):
            return NotImplemented
        return self.__key == other.get_key()

    def get_key(self) -> Any:
        """Return this node's key.

        Returns:
            Any: The key of this node.
        """
        return self.__key

    def set_key(self, key: Any) -> None:
        """Replace this node's key with ``key``.

        Args:
            key (Any): The new key to set.
        """
        self.__key = key

    def get_left(self) -> Optional['Node']:
        """Return the left child, or ``None`` if absent.

        Returns:
            Optional[Node]: The left child node.
        """
        return self.__left

    def set_left(self, node: Optional['Node']) -> None:
        """Set the left child to ``node``.

        Args:
            node (Optional[Node]): The node to set as left child.
        """
        self.__left = node

    def get_right(self) -> Optional['Node']:
        """Return the right child, or ``None`` if absent.

        Returns:
            Optional[Node]: The right child node.
        """
        return self.__right

    def set_right(self, node: Optional['Node']) -> None:
        """Set the right child to ``node``.

        Args:
            node (Optional[Node]): The node to set as right child.
        """
        self.__right = node

    def get_parent(self) -> Optional['Node']:
        """Return the parent, or ``None`` if this is a root node.

        Returns:
            Optional[Node]: The parent node.
        """
        return self.__parent

    def set_parent(self, node: Optional['Node']) -> None:
        """Set the parent node to ``node``.

        Args:
            node (Optional[Node]): The node to set as parent.
        """
        self.__parent = node

    def get_height(self) -> int:
        """Return the height of this subtree (a leaf has height zero).

        Returns:
            int: The height of the subtree.
        """
        if self.__left and self.__right:
            return max(self.__left.get_height(), self.__right.get_height()) + 1 
        elif self.__left:
            return self.__left.get_height() + 1
        elif self.__right:
            return self.__right.get_height() + 1
        else:
            return 0

    def get_depth(self) -> int:
        """Return the number of parent links between this node and the root.

        Returns:
            int: The depth of the node.
        """
        return self.__parent.get_depth() + 1 if self.__parent else 0

    def get_weight(self) -> int:
        """Return the number of nodes in this subtree, including this node.

        Returns:
            int: The weight (number of nodes).
        """
        weight = 1
        if self.__left:
            weight += self.__left.get_weight()
        if self.__right:
            weight += self.__right.get_weight()
        return weight

    def get_balance_factor(self) -> int:
        """Return left-subtree height minus right-subtree height.

        Returns:
            int: The balance factor.
        """
        left_height = self.__left.get_height() + 1 if self.__left else 0
        right_height = self.__right.get_height() + 1 if self.__right else 0
        return left_height - right_height

    def get_root(self) -> 'Node':
        """Return the root node of the tree containing this node.

        Returns:
            Node: The root node.
        """
        return self if not self.__parent else self.__parent.get_root()