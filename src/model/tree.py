class Tree:
    """Binary search tree that stores nodes ordered by their keys."""

    def __init__(self):
        """Create a tree with an optional root node.

        Args:
            root (Any, optional): The root node of the tree. Defaults to None.
        """
        self.__root = None
        self.__ids = set()

    def __contains__(self, node):
        """Return whether a node with the key exists in the tree.

        Args:
            key (Any): The key to check for.

        Returns:
            bool: True if present, False otherwise.
        """
        return node.get_id() in self.__ids

    def get_root(self):
        """Return the root node, or None when the tree is empty.

        Returns:
            Any: The root node.
        """
        return self.__root

    def get_node(self, key):
        """Find and return the node with the specified key using binary search.

        Args:
            key (Any): The key to search for.

        Returns:
            Any: The node if found, else None.
        """
        def get(root):
            if root:
                for node in self.get_levelorder_traverse():
                    if node.get_key() == root.get_key():
                        return node
            return None
        return get(self.__root)

    def add_node(self, new_node):
        """Insert new_node according to its key.

        Nodes with keys already present in the tree are ignored.

        Args:
            new_node (Any): The new node to insert.
        """
        if not self.__root:
            self.__root = new_node
            return

        def __add_node(root):
            if root.get_key() > new_node.get_key():
                if not root.get_left():
                    new_node.set_parent(root)
                    root.set_left(new_node)
                    self.__ids.add(new_node.get_id())
                else:
                    __add_node(root.get_left())
            elif root.get_key() < new_node.get_key():
                if not root.get_right():
                    new_node.set_parent(root)
                    root.set_right(new_node)
                    self.__ids.add(new_node.get_id())
                else:
                    __add_node(root.get_right())
        return __add_node(self.__root)

    def pop_node(self, key):
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
            predecessor = self.__get_maximum(node.get_left())
            self.replace_node(predecessor, predecessor.get_left())
            self.replace_node(node, predecessor)
            predecessor.set_left(node.get_left())
            predecessor.set_right(node.get_right())
            if predecessor.get_left():
                predecessor.get_left().set_parent(predecessor)
            if predecessor.get_right():
                predecessor.get_right().set_parent(predecessor)
        self.__ids.discard(node.get_id())
        return node

    def replace_node(self, old_node, new_node):
        """Replace a node in its parent link and update the new parent.

        Args:
            old_node (Any): The node to be replaced.
            new_node (Any): The node to replace with.
        """
        parent = old_node.get_parent()
        if parent is None:
            self.__root = new_node
        elif parent.get_left() is old_node:
            parent.set_left(new_node)
        elif parent.get_right() is old_node:
            parent.set_right(new_node)
        if new_node:
            new_node.set_parent(parent)

    def __get_minimum(self, root):
        """Return the smallest node in the subtree rooted at root.

        Args:
            root (Any): The root of the subtree.

        Returns:
            Any: The node with the smallest key.
        """
        if root.get_left():
            return self.__get_minimum(root.get_left())
        return root
    
    def get_minimum(self):
        """Return the smallest node in the tree, or None if empty.

        Returns:
            Any: The node with the smallest key.
        """
        if self.__root is None:
            return None
        return self.__get_minimum(self.__root)
    
    def __get_maximum(self, root):
        """Return the largest node in the subtree rooted at root.

        Args:
            root (Any): The root of the subtree.

        Returns:
            Any: The node with the largest key.
        """
        if root.get_right():
            return self.__get_maximum(root.get_right())
        return root

    def get_maximum(self):
        """Return the largest node in the tree, or None if empty.

        Returns:
            Any: The node with the largest key.
        """
        if self.__root is None:
            return None
        return self.__get_maximum(self.__root)

    def get_height(self):
        """Return the height reported by the root node.

        Returns:
            int: The height of the tree.
        """
        return self.__root.get_height() if self.__root else 0

    def get_weight(self):
        """Return the number of nodes reported by the root node.

        Returns:
            int: The total weight (node count) of the tree.
        """
        return self.__root.get_weight() if self.__root else 0

    def __rotate_left(self, node):
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

    def __rotate_right(self, node):
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

    def __balance_node(self, node):
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
                self.__rotate_left(left_child)
            self.__rotate_right(node)
            balance_factor = node.get_balance_factor()

        while balance_factor < -1:
            right_child = node.get_right()
            if right_child.get_balance_factor() > 0:
                self.__rotate_right(right_child)
            self.__rotate_left(node)
            balance_factor = node.get_balance_factor()

    def balance_branch(self, node):
        """Balance node and each of its ancestors.

        Args:
            node (Any): The start node to balance upward from.
        """
        self.__balance_node(node)
        if node.get_parent():
            self.balance_branch(node.get_parent())

    def balance_tree(self):
        """Balance every subtree until the root remains unchanged."""
        if self.__root is None:
            return

        while True:
            old_root = self.__root
            self.__balance_subtree(self.__root)

            if old_root is self.__root:
                break

    def __balance_subtree(self, node):
        """Recursively balance children before balancing node.

        Args:
            node (Any): The root of the subtree to balance.
        """
        if node is None:
            return

        left = node.get_left()
        right = node.get_right()

        self.__balance_subtree(left)
        self.__balance_subtree(right)

        self.__balance_node(node)

    def get_preorder_traverse(self):
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
        traverse(self.__root)
        return result

    def get_inorder_traverse(self):
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
        traverse(self.__root)
        return result

    def get_postorder_traverse(self):
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
        traverse(self.__root)
        return result

    def get_levelorder_traverse(self):
        """Return nodes level by level from the root downward.

        Returns:
            List[Any]: Level-order traversal of nodes.
        """
        if not self.__root:
            return []
        queue = [self.__root]
        for node in queue:
            if node.get_left():
                queue.append(node.get_left())
            if node.get_right():
                queue.append(node.get_right())
        return queue