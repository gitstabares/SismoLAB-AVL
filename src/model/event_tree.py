from .tree import Tree
from .event import Event
from .key import Key
from src.utils.intensity_color_mapper import IntensityColorMapper


class EventTree(Tree):
    """Store seismic events and thresholds for their classification."""

    def __init__(self, W:float= 48, R:float= 40, L:float= 3, autobalance= False):
        """Initialize the tree.

        Args:
            root (Optional[Any]): The root node of the tree.
            W (float): The aftershock time window in hours.
            R (float): The maximum distance for aftershock association.
            L (float): The depth threshold for costly access.
            autobalance (bool): Whether the tree should autobalance.
        """
        super().__init__()
        self._autobalance = autobalance
        self._W = W
        self._R = R
        self._L = L

    def get_autobalance(self) -> bool:
        return self._autobalance

    def set_autobalance(self, value:bool):
        self._autobalance = bool(value)
        if self._autobalance:
            self.balance_tree()

    def get_W(self) -> float:
        return self._W

    def set_W(self, W):
        self._W = W
        self.update_aftershocks()

    def get_R(self) -> float:
        return self._R

    def set_R(self, R):
        self._R = R
        self.update_aftershocks()

    def get_L(self) -> float:
        return self._L

    def set_L(self, L):
        self._L = L
        self.update_costly_access()
            
    def add_node(self, new_node:Event) -> Event:
        result = super().add_node(new_node)
        self.update_aftershocks()
        self.update_costly_access()
        if self._autobalance:
            self.balance_branch(new_node)
        return result

    def pop_node(self, key:Key) -> Event:
        result = super().pop_node(key)
        self.update_aftershocks()
        self.update_costly_access()
        if self._autobalance:
            self.balance_tree()
        return result

    def balance_branch(self, node:Event):
        result = super().balance_branch(node)
        self.update_costly_access()
        return result

    def balance_tree(self):
        result = super().balance_tree()
        self.update_costly_access()
        return result

    def update_aftershocks(self):
        """Append events that meet the aftershock association criteria."""
        for seism in self.get_levelorder_traverse():
            seism.set_aftershocks([])
            for aftershock in self.get_levelorder_traverse():
                # An aftershock must be smaller, later within W hours, and
                # closer than R to the originating event.
                if (seism.get_magnitude() > aftershock.get_magnitude() and
                    0 < (aftershock.get_date() - seism.get_date()).days < self.get_W() / 24 and
                    (aftershock.get_epicenter() - seism.get_epicenter()).get_length() < self.get_R()):
                    seism.get_aftershocks().append(aftershock)

    def update_costly_access(self):
        """Update each event's costly-access flag from its priority and depth."""
        for seism in self.get_levelorder_traverse():
            seism.set_costly_access(seism.get_key().get_priority() == 3 and seism.get_depth() > self.get_L())

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
        color_magnitude = IntensityColorMapper(-2,10)
        def _get_data(node:Event):
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
                    _get_data(node.get_left()), 
                    _get_data(node.get_right())
                ],
                "itemStyle": {
                        "color": color_magnitude.interpolate(node.get_magnitude()),  # Node color (blue)
                    },
            }
            
        return {
            "tooltip": {
                "trigger": "item",
                "triggerOn": "mousemove"
            },
            "series": [
                {
                    "type": "tree",
                    "data": [_get_data(self.get_root())],
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