from .populated_zones import PopulatedZones
from .event_tree import EventTree
from ..schemas.event import Event


class Scenario:
    """Manages seismic event trees and populated zones within a given tile size.

    Maintains AVL and BST trees for event tracking and processes incoming reports.
    """

    def __init__(self, tile_size):
        """Initialize the Scenario with a specified tile size.

        Args:
            tile_size (float): The size of tiles for populated zones.
        """
        self.__AVL = EventTree(autobalance=True)
        self.__BST = EventTree()
        self.__populated_zones = PopulatedZones(tile_size)
        self.__archived_AVL_trees = set()
        self.__archived_BST_trees = set()
        self.__eliminated_nodes = set()

    def archive_event(self, key):
        """Archive events from the trees by a given key.

        Args:
            key (Any): The key identifying the event to archive.
        """
        self.__archived_AVL_trees.add(self.__AVL.archive(key))
        self.__archived_BST_trees.add(self.__BST.archive(key))

    def insert_report(self, report):
        """Insert or update a report in the scenario's event trees.

        Args:
            report (Report): The report to process.

        Raises:
            Exception: If the ID was previously deleted.
            Exception: If there's an event with different data but the same review score.
            Exception: If the report's information is too old (lower review score).
        """
        if report.get_id() in self.__eliminated_nodes:
            raise Exception("The ID registered was used previously and currently is deleted.")
        
        new_event = Event(report, report.get_epicenter() in self.__populated_zones)
        
        if new_event not in self.__AVL:
            self.__AVL.add_node(new_event)
            self.__BST.add_node(new_event)
        else:
            actual_AVL = self.__AVL.get_node(report.get_id())
            actual_BST = self.__BST.get_node(report.get_id())
            if new_event.get_review() > actual_AVL.get_review():
                if new_event.get_key().get_tuple() != actual_AVL.get_key().get_tuple():
                    self.__AVL.pop_node(actual_AVL.get_key())
                    self.__BST.pop_node(actual_BST.get_key())
                    self.__AVL.add_node(new_event)
                    self.__BST.add_node(new_event)
                else:
                    actual_AVL.set_all(new_event)
                    actual_BST.set_all(new_event)
                self.__AVL.update_aftershocks()
                self.__AVL.update_costly_access()
                self.__BST.update_aftershocks()
                self.__BST.update_costly_access()
            elif new_event.get_review() == actual_AVL.get_review():
                if new_event.get_all() == actual_AVL.get_all():
                    actual_AVL.set_revised(True)
                    actual_BST.set_revised(True)
                    if not actual_AVL.get_origin_station():
                        actual_AVL.set_origin_station(new_event.get_origin_station())
                        actual_BST.set_origin_station(new_event.get_origin_station())
                else:
                    raise Exception("There's an event in the tree with different data and same review.")
            else:
                raise Exception("Report's information too old. There's newer information in the tree.")

    def delete_event(self, identifier):
        """Delete an event by its identifier.

        Args:
            identifier (Any): The identifier of the event to delete.
        """
        self.__AVL.pop_node(identifier)
        self.__BST.pop_node(identifier)
        self.__eliminated_nodes.add(identifier)

    def get_AVL_JSON(self):
        return self.__AVL.get_echart_dict()

    def get_BST_JSON(self):
        return self.__BST.get_echart_dict()

    def get_event_AVL(self, identifier):
        """Retrieve an event from the AVL tree.

        Args:
            identifier (Any): The identifier of the event.

        Returns:
            Any: The event node from the AVL tree.
        """
        return self.__AVL.get_node(identifier)

    def get_event_BST(self, identifier):
        """Retrieve an event from the BST tree.

        Args:
            identifier (Any): The identifier of the event.

        Returns:
            Any: The event node from the BST tree.
        """
        return self.__BST.get_node(identifier)

    def set_stress_mode(self, value):
        """Set the autobalance mode for the AVL tree.

        Args:
            value (bool): Whether autobalance should be enabled.
        """
        self.__AVL.set_autobalance(value)

    def set_W(self, W):
        """Set the W threshold for both trees.

        Args:
            W (Any): The new W threshold.
        """
        self.__AVL.set_W(W)
        self.__BST.set_W(W)

    def set_R(self, R):
        """Set the R radius for both trees.

        Args:
            R (Any): The new R radius.
        """
        self.__AVL.set_R(R)
        self.__BST.set_R(R)

    def set_L(self, L):
        """Set the L threshold for both trees.

        Args:
            L (Any): The new L threshold.
        """
        self.__AVL.set_L(L)
        self.__BST.set_L(L)