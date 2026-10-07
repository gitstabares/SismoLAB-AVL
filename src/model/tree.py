from .key import Key
from .node import Node


class Tree:
    """Binary search tree that stores nodes ordered by their keys."""

    def __init__(self):
        """Initialize an empty tree.

        The tree root is initially ``None``.
        """
        self._root = None

    def get_root(self) -> Node:
        """Return the root node of the tree.

        Returns:
            Node | None: The root node, or ``None`` if the tree is empty.
        """
        return self._root

    def set_root(self, root: Node):
        """Set the root node of the tree.

        Args:
            root (Node | None): The new root node or ``None`` for an empty tree.
        """
        self._root = root

    def __contains__(self, node: Node):
        """Return whether a node with the same key exists in the tree.

        Args:
            node (Node): The node to look up.

        Returns:
            bool: ``True`` if a node with the same key exists, otherwise
                ``False``.
        """
        return bool(self.get_node(node.get_key()))

    def get_node(self, key: Key) -> Node:
        """Return the node with the given key.

        Args:
            key (Key): The key to search for.

        Returns:
            Node | None: The matching node, or ``None`` if it is not found.
        """
        for node in self.get_levelorder_traverse():
            if node.get_key() == key:
                return node

    def add_node(self, new_node: Node) -> Node:
        """Insert a node according to its key.

        Nodes with keys already present in the tree are ignored.

        Args:
            new_node (Node): The node to insert.

        Returns:
            Node | None: The inserted node, or ``None`` when the node is a
                duplicate and is ignored.
        """
        if not self.get_root():
            self.set_root(new_node)
            return new_node

        def _add_node(root: Node) -> Node:
            """Insert the node in the subtree rooted at ``root``.

            Args:
                root (Node): The current subtree root.

            Returns:
                Node: The inserted node.
            """
            if root.get_key() > new_node.get_key():
                if not root.get_left():
                    new_node.set_parent(root)
                    root.set_left(new_node)
                    return new_node
                return _add_node(root.get_left())
            if root.get_key() < new_node.get_key():
                if not root.get_right():
                    new_node.set_parent(root)
                    root.set_right(new_node)
                    return new_node
                return _add_node(root.get_right())

        return _add_node(self.get_root())

    def pop_node(self, key: Key) -> Node:
        """Remove and return the node with the specified key.

        When a node has two children, its in-order predecessor replaces it.

        Args:
            key (Key): The key of the node to remove.

        Returns:
            Node | None: The removed node, or ``None`` if it is not found.
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

    def replace_node(self, old_node: Node, new_node: Node):
        """Replace a node and reconnect the parent relationship.

        Args:
            old_node (Node): The node to replace.
            new_node (Node | None): The replacement node, or ``None`` if the
                old node is being removed.
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

    def _get_minimum(self, root: Node) -> Node:
        """Return the smallest node in the subtree rooted at ``root``.

        Args:
            root (Node): The root of the subtree.

        Returns:
            Node: The node with the smallest key in the subtree.
        """
        if root.get_left():
            return self._get_minimum(root.get_left())
        return root

    def get_minimum(self) -> Node:
        """Return the smallest node in the tree.

        Returns:
            Node | None: The node with the smallest key, or ``None`` if the tree
                is empty.
        """
        if self.get_root() is None:
            return None
        return self._get_minimum(self.get_root())

    def _get_maximum(self, root: Node) -> Node:
        """Return the largest node in the subtree rooted at ``root``.

        Args:
            root (Node): The root of the subtree.

        Returns:
            Node: The node with the largest key in the subtree.
        """
        if root.get_right():
            return self._get_maximum(root.get_right())
        return root

    def get_maximum(self) -> Node:
        """Return the largest node in the tree.

        Returns:
            Node | None: The node with the largest key, or ``None`` if the tree
                is empty.
        """
        if self.get_root() is None:
            return None
        return self._get_maximum(self.get_root())

    def get_height(self) -> int:
        """Return the height of the tree.

        Returns:
            int: The height of the tree, or ``0`` if it is empty.
        """
        return self.get_root().get_height() if self.get_root() else 0

    def get_weight(self) -> int:
        """Return the number of nodes in the tree.

        Returns:
            int: The total number of nodes in the tree, or ``0`` if it is empty.
        """
        return self.get_root().get_weight() if self.get_root() else 0

    def _rotate_left(self, node: Node):
        """Perform a left rotation around ``node``.

        Args:
            node (Node): The node around which to rotate.
        """
        pivot = node.get_right()

        if not node or not pivot:
            return

        child = pivot.get_left()

        self.replace_node(pivot, child)
        self.replace_node(node, pivot)
        pivot.set_left(node)
        node.set_parent(pivot)

    def _rotate_right(self, node: Node):
        """Perform a right rotation around ``node``.

        Args:
            node (Node): The node around which to rotate.
        """
        pivot = node.get_left()

        if not node or not pivot:
            return

        child = pivot.get_right()

        self.replace_node(pivot, child)
        self.replace_node(node, pivot)
        pivot.set_right(node)
        node.set_parent(pivot)

    def _balance_node(self, node: Node):
        """Balance a node using rotations.

        Args:
            node (Node): The node to balance.
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

    def balance_branch(self, node: Node):
        """Balance ``node`` and each of its ancestors.

        Args:
            node (Node): The node from which to begin balancing upward.
        """
        self._balance_node(node)
        if node.get_parent():
            self.balance_branch(node.get_parent())

    def balance_tree(self):
        """Balance the tree until the root no longer changes."""
        if self.get_root() is None:
            return

        while True:
            old_root = self.get_root()
            self._balance_subtree(self.get_root())

            if old_root is self.get_root():
                break

    def _balance_subtree(self, node: Node):
        """Recursively balance the children and then the given node.

        Args:
            node (Node): The root of the subtree to balance.
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
            list[Node]: The nodes visited in preorder.
        """
        result = []

        def traverse(node):
            """Add nodes from a subtree to ``result`` in preorder."""
            if node is None:
                return
            result.append(node)
            traverse(node.get_left())
            traverse(node.get_right())

        traverse(self.get_root())
        return result

    def get_inorder_traverse(self) -> list[Node]:
        """Return nodes in left-root-right order.

        The resulting order is sorted by key.

        Returns:
            list[Node]: The nodes visited in inorder.
        """
        result = []

        def traverse(node):
            """Add nodes from a subtree to ``result`` in inorder."""
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
            list[Node]: The nodes visited in postorder.
        """
        result = []

        def traverse(node):
            """Add nodes from a subtree to ``result`` in postorder."""
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
            list[Node]: The nodes visited in level order.
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