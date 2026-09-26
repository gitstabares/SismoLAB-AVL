from .node import Node

class Tree:
    def __init__(self, root = None):
        self.__root = root

    def get_root(self):
        return self.__root

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

    def add_node(self, new_node):

        if not self.__root:
            self.__root = new_node
            return

        def __add_node(root):
            if root.get_key() > new_node.get_key():
                if not root.get_left():
                    new_node.set_parent(root)
                    root.set_left(new_node)
                else:
                    __add_node(root.get_left())
            elif root.get_key() < new_node.get_key():
                if not root.get_right():
                    new_node.set_parent(root)
                    root.set_right(new_node)
                else:
                    __add_node(root.get_right())

        __add_node(self.__root)

    def pop_node(self, key):
        node = self.get_node(key)
        if node is None:
            return None
        if not node.get_left():
            self.__replace_node(node, node.get_right())
        elif not node.get_right():
            self.__replace_node(node, node.get_left())
        else:
            predecessor = self.__get_maximum(node.get_left())
            self.__replace_node(predecessor,predecessor.get_left())
            self.__replace_node(node, predecessor)
            predecessor.set_left(node.get_left())
            predecessor.set_right(node.get_right())
            if predecessor.get_left():
                predecessor.get_left().set_parent(predecessor)
            if predecessor.get_right():
                predecessor.get_right().set_parent(predecessor)
        return node

    def __replace_node(self, old_node, new_node):
        parent = old_node.get_parent()
        if parent is None:
            self.__root = new_node
        elif parent.get_left() is old_node:
            parent.set_left(new_node)
        elif parent.get_right() is old_node:
            parent.set_right(new_node)
        if new_node:
            new_node.set_parent(parent)

    def __get_minimum(self,root):
        if root.get_left():
            return self.__get_minimum(root.get_left())
        return root
    
    def get_minimum(self):
        if self.__root is None:
            return None
        return self.__get_minimum(self.__root)
    
    def __get_maximum(self,root):
        if root.get_right():
            return self.__get_maximum(root.get_right())
        return root

    def get_maximum(self):
        if self.__root is None:
            return None
        return self.__get_maximum(self.__root)

    def get_height(self):
        return self.__root.get_height() if self.__root else 0

    def get_weight(self):
        return self.__root.get_weight() if self.__root else 0

    def __rotate_left(self, node):
        pivot = node.get_right()

        if not node or not pivot:
            return

        child = pivot.get_left()

        self.__replace_node(pivot,child)
        self.__replace_node(node,pivot)
        pivot.set_left(node)
        node.set_parent(pivot)

    def __rotate_right(self, node):
        pivot = node.get_left()

        if not node or not pivot:
            return
        
        child = pivot.get_right()

        self.__replace_node(pivot,child)
        self.__replace_node(node,pivot)
        pivot.set_right(node)
        node.set_parent(pivot)

    def __balance_node(self, node):
        if node is None:
            return None
        balance_factor = node.get_balance_factor()

        while balance_factor > 1:
            left_child = node.get_left()
            if left_child.get_balance_factor() < 0:
                self.__rotate_left(left_child)
            self.__rotate_right(node)

        while balance_factor < -1:
            right_child = node.get_right()
            if right_child.get_balance_factor() > 0:
                self.__rotate_right(right_child)
            self.__rotate_left(node)

    def balance_branch(self, node):
        self.__balance_node(node)
        if node.get_parent():
            self.balance_branch(node.get_parent())

    def balance_tree(self):
        if self.__root is None:
            return

        while True:
            old_root = self.__root
            self.__balance_subtree(self.__root)

            if old_root is self.__root:
                break

    def __balance_subtree(self, node):
        if node is None:
            return

        left = node.get_left()
        right = node.get_right()

        self.__balance_subtree(left)
        self.__balance_subtree(right)

        self.__balance_node(node)

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

    def contains(self, key):
        return self.get_node(key) is not None