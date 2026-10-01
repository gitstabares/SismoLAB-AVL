from typing import Any, Optional
from .tree import Tree


class EventTree(Tree):
    """Store seismic events and thresholds for their classification."""

    def __init__(self, root: Optional[Any] = None, W: float = 48, R: float = 40, L: float = 3, autobalance: bool = False) -> None:
        """Initialize the tree.

        Args:
            root (Optional[Any]): The root node of the tree.
            W (float): The aftershock time window in hours.
            R (float): The maximum distance for aftershock association.
            L (float): The depth threshold for costly access.
            autobalance (bool): Whether the tree should autobalance.
        """
        super().__init__(root, autobalance)
        self.__W = W
        self.__R = R
        self.__L = L

    def get_W(self) -> float:
        """Return the aftershock time-window threshold in hours.

        Returns:
            float: The aftershock time window in hours.
        """
        return self.__W

    def set_W(self, W: float) -> None:
        """Set the aftershock time-window threshold in hours.

        Args:
            W (float): The new aftershock time window in hours.
        """
        self.__W = W
        self.update_aftershocks()

    def get_R(self) -> float:
        """Return the maximum distance for aftershock association.

        Returns:
            float: The maximum distance.
        """
        return self.__R

    def set_R(self, R: float) -> None:
        """Set the maximum distance for aftershock association.

        Args:
            R (float): The new maximum distance.
        """
        self.__R = R
        self.update_aftershocks()

    def get_L(self) -> float:
        """Return the depth threshold for costly access.

        Returns:
            float: The depth threshold.
        """
        return self.__L

    def set_L(self, L: float) -> None:
        """Set the depth threshold for costly access.

        Args:
            L (float): The new depth threshold.
        """
        self.__L = L
        self.update_costly_access()

    def update_aftershocks(self) -> None:
        """Append events that meet the aftershock association criteria."""
        for seism in self.get_levelorder_traverse():
            for aftershock in self.get_levelorder_traverse():
                # An aftershock must be smaller, later within W hours, and
                # closer than R to the originating event.
                if (seism.get_magnitude() > aftershock.get_magnitude() and
                    0 < (aftershock.get_date() - seism.get_date()).days < self.__W / 24 and
                    (aftershock.get_epicenter() - seism.get_epicenter()).get_length() < self.__R):
                    seism.get_aftershocks().append(aftershock)

    def update_costly_access(self) -> None:
        """Update each event's costly-access flag from its priority and depth."""
        for seism in self.get_levelorder_traverse():
            seism.set_costly_access(seism.get_key().get_priority() == 3 and seism.get_depth() > self.__L)

    def archive(self, key: Any) -> 'EventTree':
        """Archive a node by replacing it with None, balancing if necessary.

        Args:
            key (Any): The key of the node to archive.

        Returns:
            EventTree: A new EventTree with the archived node as its root.
        """
        node = self.get_node(key)
        self.__replace_node(node, None)
        if self.__autobalance:
            self.balance_tree()
        return EventTree(root=node)