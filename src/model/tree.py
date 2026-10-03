from .key import Key
from .node import Node


class Tree:
    """Binary search tree that stores nodes ordered by their keys."""

    def __init__(self):
        """Create a tree with an optional root node.

        Args:
            root (Any, optional): The root node of the tree. Defaults to None.
        """
        self.root = None

    @property
    def root(self) -> Node:
        return self.__root

    @root.setter
    def root(self, root:Node):
        self.__root = root

    def __contains__(self, node:Node):
        return True if self.get_node(node.key) else False

    def get_node(self, key) -> Node:
        for node in self.get_levelorder_traverse():
            if node.key == key:
                return node

    def add_node(self, new_node:Node) -> Node:
        """Insert new_node according to its key.

        Nodes with keys already present in the tree are ignored.

        Args:
            new_node (Any): The new node to insert.
        """
        if not self.root:
            self.root = new_node
            return

        def __add_node(root:Node) -> Node:
            if root.key > new_node.key:
                if not root.left:
                    new_node.parent = root
                    root.left = new_node
                    return new_node
                else:
                    __add_node(root.left)
            elif root.key < new_node.key:
                if not root.right:
                    new_node.parent = root
                    root.right = new_node
                    return new_node
                else:
                    __add_node(root.right)
        return __add_node(self.root)

    def pop_node(self, key:Key) -> Node:
        """Remove and return the node with the specified key.

        When a node has two children, its in-order predecessor replaces it.
        Return None if the key is not present.

        Args:
            key (Any): The key of the node to remove.

        Returns:
            Any: The removed node, or None if not found.
        """
        node = self.get_node(key)
        if node is None:
            return None
        if not node.left:
            self.replace_node(node, node.right)
        elif not node.right:
            self.replace_node(node, node.left)
        else:
            predecessor = self.__get_maximum(node.left)
            self.replace_node(predecessor, predecessor.left)
            self.replace_node(node, predecessor)
            predecessor.left = node.left
            predecessor.right = node.right
            if predecessor.left:
                predecessor.left.parent = predecessor
            if predecessor.right:
                predecessor.right.parent = predecessor
        return node

    def replace_node(self, old_node:Node, new_node:Node):
        """Replace a node in its parent link and update the new parent.

        Args:
            old_node (Any): The node to be replaced.
            new_node (Any): The node to replace with.
        """
        parent = old_node.parent
        if parent is None:
            self.root = new_node
        elif parent.left is old_node:
            parent.left = new_node
        elif parent.right is old_node:
            parent.right = new_node
        if new_node:
            new_node.parent = parent

    def __get_minimum(self, root:Node) -> Node:
        """Return the smallest node in the subtree rooted at root.

        Args:
            root (Any): The root of the subtree.

        Returns:
            Any: The node with the smallest key.
        """
        if root.left:
            return self.__get_minimum(root.left)
        return root
    
    def get_minimum(self) -> Node:
        """Return the smallest node in the tree, or None if empty.

        Returns:
            Any: The node with the smallest key.
        """
        if self.root is None:
            return None
        return self.__get_minimum(self.root)
    
    def __get_maximum(self, root:Node) -> Node:
        """Return the largest node in the subtree rooted at root.

        Args:
            root (Any): The root of the subtree.

        Returns:
            Any: The node with the largest key.
        """
        if root.right:
            return self.__get_maximum(root.right)
        return root

    def get_maximum(self) -> Node:
        """Return the largest node in the tree, or None if empty.

        Returns:
            Any: The node with the largest key.
        """
        if self.root is None:
            return None
        return self.__get_maximum(self.root)

    def get_height(self) -> int:
        """Return the height reported by the root node.

        Returns:
            int: The height of the tree.
        """
        return self.root.get_height() if self.root else 0

    def get_weight(self) -> int:
        """Return the number of nodes reported by the root node.

        Returns:
            int: The total weight (node count) of the tree.
        """
        return self.root.get_weight() if self.root else 0

    def __rotate_left(self, node:Node):
        """Perform a left rotation around the given node.

        Args:
            node (Any): The node to rotate around.
        """
        pivot = node.right

        if not node or not pivot:
            return

        child = pivot.left

        self.replace_node(pivot, child)
        self.replace_node(node, pivot)
        pivot.left = node
        node.parent = pivot

    def __rotate_right(self, node:Node):
        """Perform a right rotation around the given node.

        Args:
            node (Any): The node to rotate around.
        """
        pivot = node.left

        if not node or not pivot:
            return
        
        child = pivot.right

        self.replace_node(pivot, child)
        self.replace_node(node, pivot)
        pivot.right = node
        node.parent = pivot

    def __balance_node(self, node:Node):
        """Rotate node until its balance factor is within range.

        Args:
            node (Any): The node to balance.
        """
        if node is None:
            return
        balance_factor = node.get_balance_factor()

        while balance_factor > 1:
            left_child = node.left
            if left_child.get_balance_factor() < 0:
                self.__rotate_left(left_child)
            self.__rotate_right(node)
            balance_factor = node.get_balance_factor()

        while balance_factor < -1:
            right_child = node.right
            if right_child.get_balance_factor() > 0:
                self.__rotate_right(right_child)
            self.__rotate_left(node)
            balance_factor = node.get_balance_factor()

    def balance_branch(self, node:Node):
        """Balance node and each of its ancestors.

        Args:
            node (Any): The start node to balance upward from.
        """
        self.__balance_node(node)
        if node.parent:
            self.balance_branch(node.parent)

    def balance_tree(self):
        """Balance every subtree until the root remains unchanged."""
        if self.root is None:
            return

        while True:
            old_root = self.root
            self.__balance_subtree(self.root)

            if old_root is self.root:
                break

    def __balance_subtree(self, node:Node):
        """Recursively balance children before balancing node.

        Args:
            node (Any): The root of the subtree to balance.
        """
        if node is None:
            return

        left = node.left
        right = node.right

        self.__balance_subtree(left)
        self.__balance_subtree(right)

        self.__balance_node(node)

    def get_preorder_traverse(self) -> list[Node]:
        """Return nodes in root-left-right order.

        Returns:
            List[Any]: Preorder traversal of nodes.
        """
        result = []
        def traverse(node):
            if node is None:
                return
            result.append(node)
            traverse(node.left)
            traverse(node.right)
        traverse(self.root)
        return result

    def get_inorder_traverse(self) -> list[Node]:
        """Return nodes in left-root-right order (sorted by key).

        Returns:
            List[Any]: Inorder traversal of nodes.
        """
        result = []
        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            result.append(node)
            traverse(node.right)
        traverse(self.root)
        return result

    def get_postorder_traverse(self) -> list[Node]:
        """Return nodes in left-right-root order.

        Returns:
            List[Any]: Postorder traversal of nodes.
        """
        result = []
        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            traverse(node.right)
            result.append(node)
        traverse(self.root)
        return result

    def get_levelorder_traverse(self) -> list[Node]:
        """Return nodes level by level from the root downward.

        Returns:
            List[Any]: Level-order traversal of nodes.
        """
        if not self.root:
            return []
        queue = [self.root]
        for node in queue:
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return queue