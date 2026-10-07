"""Tree structure for seismic events and their classification thresholds."""

from .tree import Tree
from .event import Event
from .key import Key
from src.utils.intensity_color_mapper import IntensityColorMapper


class EventTree(Tree):
    """Store seismic events and thresholds for their classification."""

    def __init__(
        self,
        W: float = 48,
        R: float = 40,
        L: float = 3,
        autobalance: bool = False,
    ):
        """Initialize the event tree.

        Args:
            W: The aftershock time window in hours.
            R: The maximum distance for aftershock association.
            L: The depth threshold for costly access.
            autobalance: Whether the tree should autobalance.
        """
        super().__init__()
        self._autobalance = autobalance
        self._W = W
        self._R = R
        self._L = L

    def get_autobalance(self) -> bool:
        """Return whether automatic balancing is enabled.

        Returns:
            True if automatic balancing is enabled; otherwise, False.
        """
        return self._autobalance

    def set_autobalance(self, value: bool) -> None:
        """Set whether automatic balancing is enabled.

        Args:
            value: The boolean value to assign.
        """
        self._autobalance = bool(value)
        if self._autobalance:
            self.balance_tree()

    def get_W(self) -> float:
        """Return the aftershock time window.

        Returns:
            The aftershock time window in hours.
        """
        return self._W

    def set_W(self, W: float) -> None:
        """Set the aftershock time window.

        Args:
            W: The new aftershock time window in hours. Zero or a falsey value
                leaves the current value unchanged.
        """
        if not W:
            return
        self._W = max(0, W)
        self.update_aftershocks()

    def get_R(self) -> float:
        """Return the maximum distance for aftershock association.

        Returns:
            The maximum distance in the tree's configured units.
        """
        return self._R

    def set_R(self, R: float) -> None:
        """Set the maximum distance for aftershock association.

        Args:
            R: The new maximum distance. Zero or a falsey value leaves the
                current value unchanged.
        """
        if not R:
            return
        self._R = max(0, R)
        self.update_aftershocks()

    def get_L(self) -> float:
        """Return the depth threshold for costly access.

        Returns:
            The depth threshold.
        """
        return self._L

    def set_L(self, L: float) -> None:
        """Set the depth threshold for costly access.

        Args:
            L: The new depth threshold. Zero or a falsey value leaves the
                current value unchanged.
        """
        if not L:
            return
        self._L = max(0, L)
        self.update_costly_access()

    def add_node(self, new_node: Event) -> Event:
        """Add a node and update derived event relationships.

        Args:
            new_node: The event to add.

        Returns:
            The added event.
        """
        result = super().add_node(new_node)
        self.update_aftershocks()
        self.update_costly_access()
        if self._autobalance:
            self.balance_branch(new_node)
        return result

    def pop_node(self, key: Key) -> Event:
        """Remove a node and update derived event relationships.

        Args:
            key: The key of the event to remove.

        Returns:
            The removed event.
        """
        result = super().pop_node(key)
        self.update_aftershocks()
        self.update_costly_access()
        if self._autobalance:
            self.balance_tree()
        return result

    def balance_branch(self, node: Event) -> Event:
        """Balance the branch rooted at a node.

        Args:
            node: The node whose branch should be balanced.

        Returns:
            The balanced node.
        """
        result = super().balance_branch(node)
        self.update_costly_access()
        return result

    def balance_tree(self) -> Tree:
        """Balance the entire tree.

        Returns:
            The balanced tree.
        """
        result = super().balance_tree()
        self.update_costly_access()
        return result

    def update_aftershocks(self) -> None:
        """Update each event's aftershock associations.

        The aftershock association criteria are: the candidate event must have
        a lower magnitude, occur later within the configured time window, and
        be closer than the configured distance threshold.
        """
        for seism in self.get_levelorder_traverse():
            seism.set_aftershocks([])
            for aftershock in self.get_levelorder_traverse():
                # An aftershock must be smaller, later within W hours, and
                # closer than R to the originating event.
                if (
                    seism.get_magnitude() > aftershock.get_magnitude()
                    and 0
                    < (aftershock.get_date() - seism.get_date()).days
                    < self.get_W() / 24
                    and (
                        aftershock.get_epicenter() - seism.get_epicenter()
                    ).get_length()
                    < self.get_R()
                ):
                    seism.get_aftershocks().append(aftershock)

    def update_costly_access(self) -> None:
        """Update each event's costly-access flag.

        An event is considered costly to access when it has priority 3 and its
        depth exceeds the configured threshold.
        """
        for seism in self.get_levelorder_traverse():
            seism.set_costly_access(
                seism.get_key().get_priority() == 3
                and seism.get_depth() > self.get_L()
            )

    def get_echart_dict(self) -> dict:
        """Build the ECharts configuration for the event tree.

        Returns:
            A dictionary containing the ECharts tree configuration and node
            data.
        """
        color_magnitude = IntensityColorMapper(1, 3, "YlOrRd")

        def _get_data(node: Event) -> dict:
            """Recursively convert a node into ECharts-compatible data.

            Args:
                node: The current node. A falsey value represents an empty
                    child position.

            Returns:
                A dictionary containing the node's label, style, children, and
                tooltip.
            """
            if not node:
                return {
                    "name": "",
                    "itemStyle": {"opacity": 0},  # Hides the circle
                    "lineStyle": {"opacity": 0},  # Hides the connecting edge
                    "label": {"show": False},  # Hides the text
                    "tooltip": {"show": False},  # Prevents user interaction
                }
            return {
                "name": f"SIS-{node.get_identifier():06d}",
                "children": (
                    [
                        _get_data(node.get_left()),
                        _get_data(node.get_right()),
                    ]
                    if node.get_left() or node.get_right()
                    else []
                ),
                "itemStyle": {
                    "color": color_magnitude.interpolate(
                        node.get_key().get_priority()
                    ),
                },
                "symbol": "diamond" if node.get_costly_access() else "circle",
                "tooltip": str(node.get_key()),
            }

        return {
            "tooltip": {
                "trigger": "item",
                "triggerOn": "mousemove",
            },
            "series": [
                {
                    "type": "tree",
                    "data": [_get_data(self.get_root())],
                    "orient": "TB",  # Top to Bottom
                    "roam": True,  # Enables zooming and dragging
                    "symbolSize": 40,  # Node size
                    "initialTreeDepth": -1,  # -1 to expand the entire tree initially
                    "expandAndCollapse": False,
                    "label": {
                        "position": "inside",
                        "verticalAlign": "middle",
                        "align": "center",
                        "color": "black",  # Text color
                        "fontSize": 14,
                    },
                    "lineStyle": {
                        "color": "#ccc",  # Edge color
                        "width": 2,
                        "curveness": 0.5,  # Curve amount
                    },
                    # Margins to prevent cropping on initial zoom
                    "top": "10%",
                    "bottom": "10%",
                    "left": "10%",
                    "right": "10%",
                }
            ],
        }