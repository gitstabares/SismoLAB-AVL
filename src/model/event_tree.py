"""Tree specialization for seismic events and their relationships."""

from model.tree import Tree

class EventTree(Tree):
    """Store seismic events and thresholds for their classification."""

    def __init__(self, root=None, W = 48, R = 40, L = 3):
        """Initialize the tree.

        W is the aftershock time window in hours, R is the maximum distance,
        and L is the depth threshold for costly access.
        """
        super().__init__(root)
        self.__W = W
        self.__R = R
        self.__L = L

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