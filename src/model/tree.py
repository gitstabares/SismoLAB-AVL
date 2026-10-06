from .key import Key
from .node import Node


class Tree:
    """Binary search tree that stores nodes ordered by their keys."""

    def __init__(self):
        """Create a tree with an optional root node.

        Args:
            root (Any, optional): The root node of the tree. Defaults to None.
        """
        self._root = None

    def get_root(self) -> Node:
        return self._root

    def set_root(self, root:Node):
        self._root = root

    def __contains__(self, node:Node):
        return True if self.get_node(node.get_key()) else False

    def get_node(self, key:Key) -> Node:
        for node in self.get_levelorder_traverse():
            if node.get_key() == key:
                return node

    def add_node(self, new_node:Node) -> Node:
        """Insert new_node according to its key.

        Nodes with keys already present in the tree are ignored.

        Args:
            new_node (Any): The new node to insert.
        """
        if not self.get_root():
            self.set_root(new_node)
            return

        def _add_node(root:Node) -> Node:
            if root.get_key() > new_node.get_key():
                if not root.get_left():
                    new_node.set_parent(root)
                    root.set_left(new_node)
                    return new_node
                else:
                    return _add_node(root.get_left())
            elif root.get_key() < new_node.get_key():
                if not root.get_right():
                    new_node.set_parent(root)
                    root.set_right(new_node)
                    return new_node
                else:
                    return _add_node(root.get_right())
        return _add_node(self.get_root())

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
        if not node.get_left():
            self.replace_node(node, node.get_right())
        elif not node.get_right():
            self.replace_node(node, node.get_left())
        else:
            predecessor = self._get_maximum(node.get_left())
            self.replace_node(predecessor, predecessor.get_left())
            self.replace_node(node, predecessor)
            predecessor.set_left(node.get_left())
            predecessor.set_right(node.get_right())
            if predecessor.get_left():
                predecessor.get_left().set_parent(predecessor)
            if predecessor.get_right():
                predecessor.get_right().set_parent(predecessor)
        return node

    def replace_node(self, old_node:Node, new_node:Node):
        """Replace a node in its parent link and update the new parent.

        Args:
            old_node (Any): The node to be replaced.
            new_node (Any): The node to replace with.
        """
        parent = old_node.get_parent()
        if parent is None:
            self.set_root(new_node)
        elif parent.get_left() is old_node:
            parent.set_left(new_node)
        elif parent.get_right() is old_node:
            parent.set_right(new_node)
        if new_node:
            new_node.set_parent(parent)

    def _get_minimum(self, root:Node) -> Node:
        """Return the smallest node in the subtree rooted at root.

        Args:
            root (Any): The root of the subtree.

        Returns:
            Any: The node with the smallest key.
        """
        if root.get_left():
            return self._get_minimum(root.get_left())
        return root
    
    def get_minimum(self) -> Node:
        """Return the smallest node in the tree, or None if empty.

        Returns:
            Any: The node with the smallest key.
        """
        if self.get_root() is None:
            return None
        return self._get_minimum(self.get_root())
    
    def _get_maximum(self, root:Node) -> Node:
        """Return the largest node in the subtree rooted at root.

        Args:
            root (Any): The root of the subtree.

        Returns:
            Any: The node with the largest key.
        """
        if root.get_right():
            return self._get_maximum(root.get_right())
        return root

    def get_maximum(self) -> Node:
        """Return the largest node in the tree, or None if empty.

        Returns:
            Any: The node with the largest key.
        """
        if self.get_root() is None:
            return None
        return self._get_maximum(self.get_root())

    def get_height(self) -> int:
        """Return the height reported by the root node.

        Returns:
            int: The height of the tree.
        """
        return self.get_root().get_height() if self.get_root() else 0

    def get_weight(self) -> int:
        """Return the number of nodes reported by the root node.

        Returns:
            int: The total weight (node count) of the tree.
        """
        return self.get_root().get_weight() if self.get_root() else 0

    def _rotate_left(self, node:Node):
        """Perform a left rotation around the given node.

        Args:
            node (Any): The node to rotate around.
        """
        pivot = node.get_right()

        if not node or not pivot:
            return

        child = pivot.get_left()

        self.replace_node(pivot, child)
        self.replace_node(node, pivot)
        pivot.set_left(node)
        node.set_parent(pivot)

    def _rotate_right(self, node:Node):
        """Perform a right rotation around the given node.

        Args:
            node (Any): The node to rotate around.
        """
        pivot = node.get_left()

        if not node or not pivot:
            return
        
        child = pivot.get_right()

        self.replace_node(pivot, child)
        self.replace_node(node, pivot)
        pivot.set_right(node)
        node.set_parent(pivot)

    def _balance_node(self, node:Node):
        """Rotate node until its balance factor is within range.

        Args:
            node (Any): The node to balance.
        """
        if node is None:
            return
        balance_factor = node.get_balance_factor()

        while balance_factor > 1:
            left_child = node.get_left()
            if left_child.get_balance_factor() < 0:
                self._rotate_left(left_child)
            self._rotate_right(node)
            balance_factor = node.get_balance_factor()

        while balance_factor < -1:
            right_child = node.get_right()
            if right_child.get_balance_factor() > 0:
                self._rotate_right(right_child)
            self._rotate_left(node)
            balance_factor = node.get_balance_factor()

    def balance_branch(self, node:Node):
        """Balance node and each of its ancestors.

        Args:
            node (Any): The start node to balance upward from.
        """
        self._balance_node(node)
        if node.get_parent():
            self.balance_branch(node.get_parent())

    def balance_tree(self):
        """Balance every subtree until the root remains unchanged."""
        if self.get_root() is None:
            return

        while True:
            old_root = self.get_root()
            self._balance_subtree(self.get_root())

            if old_root is self.get_root():
                break

    def _balance_subtree(self, node:Node):
        """Recursively balance children before balancing node.

        Args:
            node (Any): The root of the subtree to balance.
        """
        if node is None:
            return

        left = node.get_left()
        right = node.get_right()

        self._balance_subtree(left)
        self._balance_subtree(right)

        self._balance_node(node)

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
            traverse(node.get_left())
            traverse(node.get_right())
        traverse(self.get_root())
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
            traverse(node.get_left())
            result.append(node)
            traverse(node.get_right())
        traverse(self.get_root())
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
            traverse(node.get_left())
            traverse(node.get_right())
            result.append(node)
        traverse(self.get_root())
        return result

    def get_levelorder_traverse(self) -> list[Node]:
        """Return nodes level by level from the root downward.

        Returns:
            List[Any]: Level-order traversal of nodes.
        """
        if not self.get_root():
            return []
        queue = [self.get_root()]
        for node in queue:
            if node.get_left():
                queue.append(node.get_left())
            if node.get_right():
                queue.append(node.get_right())
        return queue