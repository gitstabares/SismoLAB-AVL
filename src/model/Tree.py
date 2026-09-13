from .Node import Node

class Tree:
    def __init__(self, node_type=Node):
        self.__root = None
        self.__node_type = node_type

    def get_root(self):
        return self.__root

    def set_root(self, node):
        self.__root = node
        if node:
            node.set_parent(None)

    def get_node(self, key):
        def get(root):
            if root:
                if root.get_key() == key:
                    return root
                elif root.get_key() > key:
                    return get(root.get_left())
                elif root.get_key() < key:
                    return get(root.get_right())
        return get(self.__root)

    def add_node(self, key, **kwargs):
        new_node = self.__node_type(key, **kwargs)

        if not self.__root:
            self.__root = new_node
            return

        def add(root):
            if root.get_key() > key:
                if not root.get_left():
                    new_node.set_parent(root)
                    root.set_left(new_node)
                else:
                    add(root.get_left())
            elif root.get_key() < key:
                if not root.get_right():
                    new_node.set_parent(root)
                    root.set_right(new_node)
                else:
                    add(root.get_right())

        add(self.__root)

    def delete_node(self, key):
        node = self.get_node(key)

        if node is None:
            return None

        parent = node.get_parent()

        if node.get_left() is None:
            replacement = node.get_right()
            self.__replace_node(node, replacement)
            start_node = replacement if replacement else parent

        elif node.get_right() is None:
            replacement = node.get_left()
            self.__replace_node(node, replacement)
            start_node = replacement if replacement else parent

        else:
            successor = self.__get_minimum(node.get_right())
            successor_parent = successor.get_parent()

            if successor_parent != node:
                successor_right = successor.get_right()
                self.__replace_node(successor, successor_right)

                successor.set_right(node.get_right())

                if successor.get_right():
                    successor.get_right().set_parent(successor)

                start_node = successor_parent
            else:
                start_node = successor

            self.__replace_node(node, successor)

            successor.set_left(node.get_left())

            if successor.get_left():
                successor.get_left().set_parent(successor)

            self.__update_height(successor)

        node.set_left(None)
        node.set_right(None)
        node.set_parent(None)

        if start_node:
            self.__update_heights_upward(start_node)
            self.balance_branch(start_node)

        return node

    def __replace_node(self, old_node, new_node):
        parent = old_node.get_parent()

        if parent is None:
            self.set_root(new_node)
        elif parent.get_left() is old_node:
            parent.set_left(new_node)
            if new_node:
                new_node.set_parent(parent)
        else:
            parent.set_right(new_node)
            if new_node:
                new_node.set_parent(parent)

    def get_minimum(self):
        if self.__root is None:
            return None
        def get(root):
            if root.get_left():
                return get(root.get_left())
            return root
        return self.get(self.__root)

    def get_maximum(self):
        if self.__root is None:
            return None
        def get(root):
            if root.get_right():
                return get(root.get_right())
            return root
        return self.get(self.__root)

    def get_height(self):
        return self.__root.get_height() if self.__root else 0

    def get_balance_factor(self, node):
        if node is None:
            return 0

        return node.get_balance_factor()

    def rotate_left(self, node):
        if node is None or node.get_right() is None:
            return node

        pivot = node.get_right()
        parent = node.get_parent()
        pivot_left = pivot.get_left()

        pivot.set_parent(parent)

        if parent is None:
            self.__root = pivot
        elif parent.get_left() is node:
            parent.set_left(pivot)
        else:
            parent.set_right(pivot)

        pivot.set_left(node)
        node.set_parent(pivot)

        node.set_right(pivot_left)

        if pivot_left:
            pivot_left.set_parent(node)

        self.__update_height(node)
        self.__update_height(pivot)

        return pivot

    def rotate_right(self, node):
        if node is None or node.get_left() is None:
            return node

        pivot = node.get_left()
        parent = node.get_parent()
        pivot_right = pivot.get_right()

        pivot.set_parent(parent)

        if parent is None:
            self.__root = pivot
        elif parent.get_left() is node:
            parent.set_left(pivot)
        else:
            parent.set_right(pivot)

        pivot.set_right(node)
        node.set_parent(pivot)

        node.set_left(pivot_right)

        if pivot_right:
            pivot_right.set_parent(node)

        self.__update_height(node)
        self.__update_height(pivot)

        return pivot

    def balance_node(self, node):
        if node is None:
            return None

        self.__update_height(node)

        balance_factor = node.get_balance_factor()

        if balance_factor > 1:
            left_child = node.get_left()

            if left_child and left_child.get_balance_factor() < 0:
                self.rotate_left(left_child)

            return self.rotate_right(node)

        if balance_factor < -1:
            right_child = node.get_right()

            if right_child and right_child.get_balance_factor() > 0:
                self.rotate_right(right_child)

            return self.rotate_left(node)

        return node

    def balance_branch(self, node):
        current = node

        while current:
            parent = current.get_parent()
            new_root = self.balance_node(current)

            if new_root.get_parent() is None:
                self.__root = new_root

            current = new_root.get_parent() if new_root else parent

    def balance_tree(self):
        if self.__root is None:
            return None

        self.__balance_subtree(self.__root)

        while True:
            old_root = self.__root
            self.__balance_subtree(self.__root)

            if old_root is self.__root:
                break

        self.__update_heights_upward(self.__root)

        return self.__root

    def __balance_subtree(self, node):
        if node is None:
            return

        left = node.get_left()
        right = node.get_right()

        self.__balance_subtree(left)
        self.__balance_subtree(right)

        self.__update_height(node)
        self.balance_node(node)

    def get_preorder_traverse(self):
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
        if not self.__root:
            return []
        queue = [self.__root]
        for node in queue:
            if node.get_left():
                queue.append(node.get_left())
            if node.get_right():
                queue.append(node.get_right())
        return queue

    def clear(self):
        self.__root = None

    def is_empty(self):
        return self.__root is None

    def contains(self, key):
        return self.get_node(key) is not None