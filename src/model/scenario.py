from .populated_zones import PopulatedZones
from .event_tree import EventTree
from .event import Event
from .key import Key
from .report import Report

class Scenario:
    """Manages seismic event trees and populated zones within a given tile size.
    Maintains AVL and BST trees for event tracking and processes incoming reports.
    """

    def __init__(self):
        """Initialize the Scenario with a specified tile size.
        """
        self.AVL = EventTree(autobalance=True)
        self.BST = EventTree()
        self.populated_zones = PopulatedZones()
        self.archived_AVL_trees = set()
        self.eliminated_ids = set()

    @property
    def AVL(self) -> EventTree:
        return self.__AVL

    @AVL.setter
    def AVL(self, tree:EventTree):
        self.__AVL = tree

    @property
    def BST(self) -> EventTree:
        return self.__BST

    @BST.setter
    def BST(self, tree:EventTree):
        self.__BST = tree

    @property
    def populated_zones(self) -> PopulatedZones:
        return self.__populated_zones

    @populated_zones.setter
    def populated_zones(self, zones:PopulatedZones):
        self.__populated_zones = zones

    @property
    def archived_AVL_trees(self) -> set:
        return self.__archived_AVL_trees

    @archived_AVL_trees.setter
    def archived_AVL_trees(self, value:set):
        self.__archived_AVL_trees = value

    @property
    def eliminated_ids(self) -> set:
        return self.__eliminated_ids

    @eliminated_ids.setter
    def eliminated_ids(self, value:set):
        self.__eliminated_ids = value

    def archive_event(self, key:Key):
        """Archive events from the trees by a given key.

        Args:
            key (Any): The key identifying the event to archive.
        """
        node = self.AVL.get_node(key)
        if not node:
            return
        self.AVL.replace_node(node, None)
        if self.AVL.autobalance:
            self.AVL.balance_tree()
        tree = EventTree()
        tree.add_node(node)
        self.archived_AVL_trees.add(tree)

    def insert_report(self, report:Report):
        """Insert or update a report in the scenario's event trees.

        Args:
            report (Report): The report to process.

        Raises:
            Exception: If the ID was previously deleted.
            Exception: If there's an event with different data but the same review score.
            Exception: If the report's information is too old (lower review score).
        """
        if report.identifier in self.eliminated_ids:
            raise Exception("The ID registered was used previously and currently is deleted.")

        new_event = Event(report)

        for tree in self.archived_AVL_trees:
            if new_event in tree:
                self.AVL.add_node(Event(report))
                self.BST.add_node(Event(report))
                self.archived_AVL_trees.discard(tree)
                return
        
        if new_event not in self.AVL:
            self.AVL.add_node(Event(report))
            self.BST.add_node(Event(report))
        else:
            actual_AVL = self.AVL.get_node(report.identifier)
            actual_BST = self.BST.get_node(report.identifier)
            if new_event.review > actual_AVL.review:
                if new_event.key != actual_AVL.key:
                    self.AVL.pop_node(report.identifier)
                    self.BST.pop_node(report.identifier)
                    self.AVL.add_node(Event(report))
                    self.BST.add_node(Event(report))
                else:
                    actual_AVL.set_data(report)
                    actual_BST.set_data(report)
                self.AVL.update_aftershocks()
                self.AVL.update_costly_access()
                self.BST.update_aftershocks()
                self.BST.update_costly_access()
            elif new_event.review == actual_AVL.review:
                if new_event.get_data() == actual_AVL.get_data():
                    actual_AVL.revised = True
                    actual_BST.revised = True
                    if not actual_AVL.station:
                        actual_AVL.station = new_event.station
                        actual_BST.station = new_event.station
                else:
                    raise Exception("There's an event in the tree with different data and same review.")
            else:
                raise Exception("Report's information too old. There's newer information in the tree.")

    def delete_event(self, identifier):
        """Delete an event by its identifier.

        Args:
            identifier (Any): The identifier of the event to delete.
        """
        self.AVL.pop_node(identifier)
        self.BST.pop_node(identifier)
        self.eliminated_ids.add(identifier)

    def get_AVL_JSON(self):
        return self.AVL.get_echart_dict()

    def get_BST_JSON(self):
        return self.BST.get_echart_dict()

    def get_event_AVL(self, identifier):
        """Retrieve an event from the AVL tree.

        Args:
            identifier (Any): The identifier of the event.

        Returns:
            Any: The event node from the AVL tree.
        """
        return self.AVL.get_node(identifier)

    def get_event_BST(self, identifier):
        """Retrieve an event from the BST tree.

        Args:
            identifier (Any): The identifier of the event.

        Returns:
            Any: The event node from the BST tree.
        """
        return self.BST.get_node(identifier)

    def set_stress_mode(self, value):
        """Set the autobalance mode for the AVL tree.

        Args:
            value (bool): Whether autobalance should be enabled.
        """
        self.AVL.set_autobalance(not value)

    def set_W(self, W):
        """Set the W threshold for both trees.

        Args:
            W (Any): The new W threshold.
        """
        self.AVL.W = W
        self.BST.W = W

    def set_R(self, R):
        """Set the R radius for both trees.

        Args:
            R (Any): The new R radius.
        """
        self.AVL.R = R
        self.BST.R = R

    def set_L(self, L):
        """Set the L threshold for both trees.

        Args:
            L (Any): The new L threshold.
        """
        self.AVL.L = L
        self.BST.L = L