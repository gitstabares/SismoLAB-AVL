from .tree import Tree
from .event import Event
from .key import Key


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
        self.autobalance = bool(autobalance)
        self.W = W
        self.R = R
        self.L = L

    @property
    def autobalance(self) -> bool:
        return self.__autobalance

    @autobalance.setter
    def autobalance(self, value:bool):
        self.__autobalance = value
        if value:
            self.balance_tree()

    @property
    def W(self) -> float:
        return self.__W

    @W.setter
    def W(self,W):
        self.__W = W
        self.update_aftershocks()

    @property
    def R(self) -> float:
        return self.__R

    @R.setter
    def R(self,R):
        self.__R = R
        self.update_aftershocks()

    @property
    def L(self) -> float:
        return self.__L

    @L.setter
    def L(self,L):
        self.__L = L
        self.update_costly_access()

    def add_node(self, new_node:Event) -> Event:
        result = super().add_node(new_node)
        self.update_aftershocks()
        self.update_costly_access()
        if self.__autobalance:
            self.balance_branch(new_node)
        return result

    def pop_node(self, key) -> Event:
        result = super().pop_node(key)
        self.update_aftershocks()
        self.update_costly_access()
        if self.__autobalance:
            self.balance_tree()
        return result

    def balance_branch(self, node):
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
            seism.aftershocks = []
            for aftershock in self.get_levelorder_traverse():
                # An aftershock must be smaller, later within W hours, and
                # closer than R to the originating event.
                if (seism.magnitude > aftershock.magnitude and
                    0 < (aftershock.date - seism.date).days < self.W / 24 and
                    (aftershock.epicenter - seism.epicenter).length < self.R):
                    seism.aftershocks.append(aftershock)

    def update_costly_access(self):
        """Update each event's costly-access flag from its priority and depth."""
        for seism in self.get_levelorder_traverse():
            seism.costly_access = seism.key.priority == 3 and seism.depth > self.L

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