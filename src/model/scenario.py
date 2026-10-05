from .populated_zones import PopulatedZones
from .event_tree import EventTree
from .event import Event
from .key import Key
from .report import Report
import datetime as dt

class Scenario:
    """Manages seismic event trees and populated zones within a given tile size.
    Maintains AVL and BST trees for event tracking and processes incoming reports.
    """

    def __init__(self):
        """Initialize the Scenario with a specified tile size.
        """
        self.set_AVL(EventTree(autobalance=True))
        self.set_BST(EventTree())
        self.set_populated_zones(PopulatedZones())
        self.set_archived_AVL_trees(set())
        self.set_eliminated_ids(set())
        self.set_current_time(dt.datetime.now())
        
    def get_AVL(self) -> EventTree:
        return self._AVL

    def set_AVL(self, tree: EventTree):
        self._AVL = tree

    def get_BST(self) -> EventTree:
        return self._BST

    def set_BST(self, tree: EventTree):
        self._BST = tree

    def get_populated_zones(self) -> PopulatedZones:
        return self._populated_zones

    def set_populated_zones(self, zones: PopulatedZones):
        self._populated_zones = zones

    def get_archived_AVL_trees(self) -> set:
        return self._archived_AVL_trees

    def set_archived_AVL_trees(self, value: set):
        self._archived_AVL_trees = value

    def get_eliminated_ids(self) -> set:
        return self._eliminated_ids

    def set_eliminated_ids(self, value: set):
        self._eliminated_ids = value

    def get_current_time(self) -> dt.datetime:
        return self._current_time

    def set_current_time(self,time:dt.datetime):
        self._current_time = time

    def archive_event(self, key:Key):
        """Archive events from the trees by a given key.

        Args:
            key (Any): The key identifying the event to archive.
        """
        node = self.get_AVL().get_node(key)
        if not node:
            return
        self.get_AVL().replace_node(node, None)
        if self.get_AVL().get_autobalance():
            self.get_AVL().balance_tree()
        tree = EventTree()
        tree.add_node(node)
        self.get_archived_AVL_trees().add(tree)

    def insert_report(self, report:Report):
        """Insert or update a report in the scenario's event trees.

        Args:
            report (Report): The report to process.

        Raises:
            Exception: If the ID was previously deleted.
            Exception: If there's an event with different data but the same review score.
            Exception: If the report's information is too old (lower review score).
        """
        if report.get_identifier() in self.get_eliminated_ids():
            raise Exception("The ID registered was used previously and currently is deleted.")

        new_event = Event(report)

        for tree in self.get_archived_AVL_trees():
            if new_event in tree:
                self.get_AVL().add_node(Event(report))
                self.get_BST().add_node(Event(report))
                self.get_archived_AVL_trees().discard(tree)
                return
        
        if new_event not in self.get_AVL():
            self.get_AVL().add_node(Event(report))
            self.get_BST().add_node(Event(report))
        else:
            actual_AVL = self.get_AVL().get_node(report.get_key())
            actual_BST = self.get_BST().get_node(report.get_key())
            if new_event.get_review() > actual_AVL.get_review():
                if new_event.get_key() != actual_AVL.get_key():
                    self.get_AVL().pop_node(report.get_key())
                    self.get_BST().pop_node(report.get_key())
                    self.get_AVL().add_node(Event(report))
                    self.get_BST().add_node(Event(report))
                else:
                    actual_AVL.set_data(report)
                    actual_BST.set_data(report)
                self.get_AVL().update_aftershocks()
                self.get_AVL().update_costly_access()
                self.get_BST().update_aftershocks()
                self.get_BST().update_costly_access()
            elif new_event.get_review() == actual_AVL.get_review():
                if new_event.get_data() == actual_AVL.get_data():
                    actual_AVL.set_revised(True)
                    actual_BST.set_revised(True)
                    if not actual_AVL.get_station():
                        actual_AVL.set_station(new_event.get_station())
                        actual_BST.set_station(new_event.get_station())
                else:
                    raise Exception("There's an event in the tree with different data and same review.")
            else:
                raise Exception("Report's information too old. There's newer information in the tree.")

    def delete_event(self, identifier):
        """Delete an event by its identifier.

        Args:
            identifier (Any): The identifier of the event to delete.
        """
        self.get_AVL().pop_node(identifier)
        self.get_BST().pop_node(identifier)
        self.get_eliminated_ids().add(identifier)

    def get_AVL_JSON(self):
        return self.get_AVL().get_echart_dict()

    def get_BST_JSON(self):
        return self.get_BST().get_echart_dict()

    def get_event_AVL(self, identifier):
        """Retrieve an event from the AVL tree.

        Args:
            identifier (Any): The identifier of the event.

        Returns:
            Any: The event node from the AVL tree.
        """
        return self.get_AVL().get_node(identifier)

    def get_event_BST(self, identifier):
        """Retrieve an event from the BST tree.

        Args:
            identifier (Any): The identifier of the event.

        Returns:
            Any: The event node from the BST tree.
        """
        return self.get_BST().get_node(identifier)

    def set_stress_mode(self, value):
        """Set the autobalance mode for the AVL tree.

        Args:
            value (bool): Whether autobalance should be enabled.
        """
        self.get_AVL().set_autobalance(not value)

    def set_W(self, W):
        """Set the W threshold for both trees.

        Args:
            W (Any): The new W threshold.
        """
        self.get_AVL().set_W(W)
        self.get_BST().set_W(W)

    def set_R(self, R):
        """Set the R radius for both trees.

        Args:
            R (Any): The new R radius.
        """
        self.get_AVL().set_R(R)
        self.get_BST().set_R(R)

    def set_L(self, L):
        """Set the L threshold for both trees.

        Args:
            L (Any): The new L threshold.
        """
        self.get_AVL().set_L(L)
        self.get_BST().set_L(L)