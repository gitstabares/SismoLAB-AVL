from typing import Any, Dict

def get_echart_dict(tree: Any) -> Dict[str, Any]:
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
    
    def __get_data(node: Any) -> Dict[str, Any]:
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
                "data": [__get_data(tree.get_root())],
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