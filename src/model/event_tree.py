from hmac import new

from .tree import Tree


class EventTree(Tree):
    """Store seismic events and thresholds for their classification."""

    def __init__(self, W= 48, R= 40, L= 3, autobalance= False):
        """Initialize the tree.

        Args:
            root (Optional[Any]): The root node of the tree.
            W (float): The aftershock time window in hours.
            R (float): The maximum distance for aftershock association.
            L (float): The depth threshold for costly access.
            autobalance (bool): Whether the tree should autobalance.
        """
        super().__init__()
        self.__autobalance = bool(autobalance)
        self.__W = W
        self.__R = R
        self.__L = L
        
    def get_autobalance(self):
        """Return whether automatic balancing is enabled.

        Returns:
            bool: True if autobalance is enabled, False otherwise.
        """
        return self.__autobalance

    def set_autobalance(self, value):
        """Set whether automatic balancing is enabled.

        Args:
            value (bool): The new autobalance state.
        """
        self.__autobalance = value
        if value:
            self.balance_tree()

    def get_W(self):
        """Return the aftershock time-window threshold in hours.

        Returns:
            float: The aftershock time window in hours.
        """
        return self.__W

    def set_W(self, W):
        """Set the aftershock time-window threshold in hours.

        Args:
            W (float): The new aftershock time window in hours.
        """
        self.__W = W
        self.update_aftershocks()

    def get_R(self):
        """Return the maximum distance for aftershock association.

        Returns:
            float: The maximum distance.
        """
        return self.__R

    def set_R(self, R):
        """Set the maximum distance for aftershock association.

        Args:
            R (float): The new maximum distance.
        """
        self.__R = R
        self.update_aftershocks()

    def get_L(self):
        """Return the depth threshold for costly access.

        Returns:
            float: The depth threshold.
        """
        return self.__L

    def set_L(self, L):
        """Set the depth threshold for costly access.

        Args:
            L (float): The new depth threshold.
        """
        self.__L = L
        self.update_costly_access()

    def add_node(self, new_node):
        result = super().add_node(new_node)
        self.update_aftershocks()
        self.update_costly_access()
        if self.__autobalance:
            self.balance_branch(new_node)
        return result

    def pop_node(self, key):
        result = super().pop_node(key)
        self.update_aftershocks()
        self.update_costly_access()
        self.__ids.discard()
        if self.__autobalance:
            self.balance_tree()
        return result

    def update_aftershocks(self):
        """Append events that meet the aftershock association criteria."""
        for seism in self.get_levelorder_traverse():
            seism.set_aftershocks([])
            for aftershock in self.get_levelorder_traverse():
                # An aftershock must be smaller, later within W hours, and
                # closer than R to the originating event.
                if (seism.get_magnitude() > aftershock.get_magnitude() and
                    0 < (aftershock.get_date() - seism.get_date()).days < self.__W / 24 and
                    (aftershock.get_epicenter() - seism.get_epicenter()).get_length() < self.__R):
                    seism.get_aftershocks().append(aftershock)

    def update_costly_access(self):
        """Update each event's costly-access flag from its priority and depth."""
        for seism in self.get_levelorder_traverse():
            seism.set_costly_access(seism.get_key().get_priority() == 3 and seism.get_depth() > self.__L)

    def archive(self, key):
        """Archive a node by replacing it with None, balancing if necessary.

        Args:
            key (Any): The key of the node to archive.

        Returns:
            EventTree: A new EventTree with the archived node as its root.
        """
        node = self.get_node(key)
        self.replace_node(node, None)
        if self.__autobalance:
            self.balance_tree()
        return EventTree(root=node)

    def get_echart_dict(self):
        """
        Generates an ECharts-compatible dictionary representation of a tree structure.

        This function configures an ECharts tree series for visualization, traversing
        the provided tree to build the hierarchical data format required.

        Args:
            tree (Any): The tree object containing the root node to visualize. 
                        Must have a `get_root()` method.

        Returns:
            Dict[str, Any]: A dictionary containing the ECharts configuration and tree data.
        """
        
        def __get_data(node):
            """
            Recursively extracts data from a tree node to format it for ECharts.

            Args:
                node (Any): The current node being processed. Must have `get_left()` 
                            and `get_right()` methods if not None.

            Returns:
                Dict[str, Any]: A dictionary representing the node and its children.
            """
            if not node:
                return {
                    "name": "", 
                    "itemStyle": {"opacity": 0}, # Hides the circle
                    "lineStyle": {"opacity": 0}, # Hides the connecting edge
                    "label": {"show": False},    # Hides the text
                    "tooltip": {"show": False}   # Prevents user interaction
                }
            return {
                'name': str(node),
                'children': [
                    __get_data(node.get_left()), 
                    __get_data(node.get_right())
                ]
            }
            
        return {
            "tooltip": {
                "trigger": "item",
                "triggerOn": "mousemove"
            },
            "series": [
                {
                    "type": "tree",
                    "data": [__get_data(self.get_root())],
                    "orient": "TB",          # Top to Bottom
                    "roam": True,            # Enables zooming and dragging
                    "symbolSize": 40,        # Node size
                    "initialTreeDepth": -1,  # -1 to expand the entire tree initially
                    "label": {
                        "position": "inside",
                        "verticalAlign": "middle",
                        "align": "center",
                        "color": "black",    # Text color
                        "fontSize": 14
                    },
                    "symbol": "circle",
                    "itemStyle": {
                        "color": "#3b82f6",  # Node color (blue)
                        "borderColor": "#1d4ed8"
                    },
                    "lineStyle": {
                        "color": "#ccc",     # Edge color
                        "width": 2,
                        "curveness": 0.5     # Curve amount
                    },
                    # Margins to prevent cropping on initial zoom
                    "top": "10%",
                    "bottom": "10%",
                    "left": "10%",
                    "right": "10%"
                }
            ]
        }