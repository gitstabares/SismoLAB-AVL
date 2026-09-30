from .tree import Tree


class EventTree(Tree):
    """Store seismic events and thresholds for their classification."""

    def __init__(self, root=None, W = 48, R = 40, L = 3, autobalance = False):
        """Initialize the tree.

        W is the aftershock time window in hours, R is the maximum distance,
        and L is the depth threshold for costly access.
        """
        super().__init__(root, autobalance)
        self.__W = W
        self.__R = R
        self.__L = L
        self.__id_list = set()

    def get_W(self):
        """Return the aftershock time-window threshold in hours."""
        return self.__W

    def set_W(self, W):
        """Set the aftershock time-window threshold in hours."""
        self.__W = W

    def get_R(self):
        """Return the maximum distance for aftershock association."""
        return self.__R

    def set_R(self, R):
        """Set the maximum distance for aftershock association."""
        self.__R = R

    def get_L(self):
        """Return the depth threshold for costly access."""
        return self.__L

    def set_L(self, L):
        """Set the depth threshold for costly access."""
        self.__L = L

    def add_node(self, new_node):
        self.__id_list.add(new_node.get_id())        
        return super().add_node(new_node)
    
    def pop_node(self, key):
        node = self.get_node(key)
        if node:
            self.__id_list.discard(node.get_id())
        return super().pop_node(key)

    def __contains__(self, key):
        return key in self.__id_list

    def update_aftershocks(self):
        """Append events that meet the aftershock association criteria."""
        for seism in self.get_levelorder_traverse():
            for aftershock in self.get_levelorder_traverse():
                # An aftershock must be smaller, later within W hours, and
                # closer than R to the originating event.
                if seism.get_magnitude() > aftershock.get_magnitude() and 0 < (aftershock.get_date() - seism.get_date()).days < self.__W/24 and (aftershock.get_epicenter() - seism.get_epicenter()).get_length() < self.__R:
                    seism.get_aftershocks().append(aftershock)

    def update_costly_access(self):
        """Update each event's costly-access flag from its priority and depth."""
        for seism in self.get_levelorder_traverse():
            seism.set_costly_access(seism.get_key().get_priority() == 3 and seism.get_depth() > self.__L)

    def archive(self, node):
        self.__replace_node(node, None)
        if self.__autobalance:
            self.balance_tree()
        return EventTree(root=node)