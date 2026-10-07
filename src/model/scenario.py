"""Scenario state and event-management logic for seismic data.

This module coordinates the AVL and BST event trees, populated zones,
archived trees, deleted identifiers, queued reports, and undo/redo history.
"""

from src.utils import *
from .populated_zones import PopulatedZones
from .event_tree import EventTree
from .event import Event
from .key import Key
from .report import Report
import datetime as dt
from collections import deque
import copy


class Scenario:
    """Manage seismic event trees and related scenario state.

    The scenario maintains synchronized AVL and BST trees, accumulates reports,
and tracks archived, deleted, and queued data while supporting burst mode and
    undo/redo operations.
    """

    def __init__(self):
        """Initialize the scenario and its data structures.

        Returns:
            None: Initializes the trees, queues, timestamps, and state sets.
        """
        self.set_AVL(EventTree(autobalance=True))
        self.set_BST(EventTree())
        self.set_populated_zones(PopulatedZones())
        self.set_archived_trees(set())
        self.set_eliminated_ids(set())
        self.set_current_time(dt.datetime.now())
        self.reports_queue = deque()
        self.set_burst_mode(False)
        self.undo_queue = deque(maxlen=3)
        self.redo_queue = deque(maxlen=3)
        self.set_T(72)
        
    def get_AVL(self) -> EventTree:
        """Return the AVL event tree.

        Returns:
            EventTree: The AVL tree containing scenario events.
        """
        return self._AVL

    def set_AVL(self, tree: EventTree):
        """Set the AVL event tree.

        Args:
            tree (EventTree): The new AVL tree.
        """
        self._AVL = tree

    def get_BST(self) -> EventTree:
        """Return the BST event tree.

        Returns:
            EventTree: The BST tree containing scenario events.
        """
        return self._BST

    def set_BST(self, tree: EventTree):
        """Set the BST event tree.

        Args:
            tree (EventTree): The new BST tree.
        """
        self._BST = tree

    def get_populated_zones(self) -> PopulatedZones:
        """Return the populated-zones collection.

        Returns:
            PopulatedZones: The scenario's populated zone data.
        """
        return self._populated_zones

    def set_populated_zones(self, zones: PopulatedZones):
        """Set the populated-zones collection.

        Args:
            zones (PopulatedZones): The new populated zone data.
        """
        self._populated_zones = zones

    def get_archived_trees(self) -> set:
        """Return the archived event trees.

        Returns:
            set: The set of archived event trees.
        """
        return self._archived_trees

    def set_archived_trees(self, value: set):
        """Set the archived event trees.

        Args:
            value (set): The new archived-tree set.
        """
        self._archived_trees = value

    def get_eliminated_ids(self) -> set:
        """Return identifiers that were deleted from the scenario.

        Returns:
            set: The eliminated identifier set.
        """
        return self._eliminated_ids

    def set_eliminated_ids(self, value: set):
        """Set the eliminated identifier set.

        Args:
            value (set): The new eliminated identifier set.
        """
        self._eliminated_ids = value

    def get_current_time(self) -> dt.datetime:
        """Return the scenario's current time.

        Returns:
            datetime.datetime: The current scenario time.
        """
        return self._current_time

    def set_current_time(self, time: dt.datetime):
        """Set the scenario current time.

        Args:
            time (datetime.datetime): The new current time.
        """
        self._current_time = time

    def get_burst_mode(self) -> bool:
        """Return whether burst mode is enabled.

        Returns:
            bool: True if queued reports are processed in burst mode.
        """
        return self._burst_mode

    def set_burst_mode(self, value: bool):
        """Enable or disable burst mode and process queued reports.

        Args:
            value (bool): Whether burst mode should be enabled.
        """
        self._burst_mode = value
        while self.reports_queue:
            try:
                self.insert_report(self.reports_queue.popleft())
            except:
                pass
        self.refresh()

    def archive_event(self, key: Key):
        """Archive an event from the AVL tree.

        Args:
            key (Key): The key identifying the event to archive.
        """
        node = self.get_AVL().get_node(key)
        if not node:
            return

        def check_archive_subtree(node:Event):
            if node.get_priority() != 1 or self.get_current_time() - node.get_date() <= self._T:
                return False
            response = True
            if node.get_left():
                response *= check_archive_subtree(node.get_left())
            if node.get_right():
                response *= check_archive_subtree(node.get_right())
            return bool(response)

        if not check_archive_subtree(node):
            raise Exception("Event can't be archived")
        
        self.get_AVL().replace_node(node, None)
        if self.get_AVL().get_autobalance():
            self.get_AVL().balance_tree()
        tree = EventTree()
        tree.add_node(node)
        self.get_archived_trees().add(tree)
        self.refresh()

    def add_report(self, report: Report):
        """Queue or insert a report depending on burst mode.

        Args:
            report (Report): The report to process.
        """
        if self.get_burst_mode():
            self.commit()
            self.reports_queue.append(report)
            self.refresh()
        else:
            self.insert_report(report)

    def insert_report(self, report: Report):
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

        for tree in self.get_archived_trees():
            if new_event in tree:
                self.commit()
                self.get_AVL().add_node(Event(report))
                self.get_BST().add_node(Event(report))
                self.get_archived_trees().discard(tree)
                return
        
        if new_event not in self.get_AVL():
            self.commit()
            self.get_AVL().add_node(Event(report))
            self.get_BST().add_node(Event(report))
        else:
            actual_AVL = self.get_AVL().get_node(report.get_key())
            actual_BST = self.get_BST().get_node(report.get_key())
            if new_event.get_review() > actual_AVL.get_review():
                self.commit()
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
                    self.commit()
                    actual_AVL.set_revised(True)
                    actual_BST.set_revised(True)
                    if not actual_AVL.get_station():
                        actual_AVL.set_station(new_event.get_station())
                        actual_BST.set_station(new_event.get_station())
                    raise Exception("Event with the same data was confirmed in the tree as revised.")
                else:
                    raise Exception("There's an event in the tree with different data and same review.")
            else:
                raise Exception("Report's information too old. There's newer information in the tree.")
        self.refresh()

    def delete_event(self, key: Key):
        """Delete an event from both trees.

        Args:
            key (Key): The key identifying the event to delete.
        """
        self.commit()
        identifier = key.get_identifier()
        self.get_AVL().pop_node(key)
        self.get_BST().pop_node(key)
        self.get_eliminated_ids().add(identifier)
        self.refresh()

    def get_AVL_JSON(self):
        """Return the AVL tree as an ECharts-compatible dictionary.

        Returns:
            dict: Serialized AVL tree data.
        """
        return self.get_AVL().get_echart_dict()

    def get_BST_JSON(self):
        """Return the BST tree as an ECharts-compatible dictionary.

        Returns:
            dict: Serialized BST tree data.
        """
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
        """Set the AVL tree's autobalance mode.

        Args:
            value (bool): Whether autobalance should be disabled.
        """
        self.get_AVL().set_autobalance(not value)
        self.refresh()

    def set_W(self, W):
        """Set the W threshold for both trees.

        Args:
            W (Any): The new W threshold.
        """
        self.get_AVL().set_W(W)
        self.get_BST().set_W(W)
        self.refresh()

    def set_R(self, R):
        """Set the R radius for both trees.

        Args:
            R (Any): The new R radius.
        """
        self.get_AVL().set_R(R)
        self.get_BST().set_R(R)
        self.refresh()

    def set_L(self, L):
        """Set the L threshold for both trees.

        Args:
            L (Any): The new L threshold.
        """
        self.get_AVL().set_L(L)
        self.get_BST().set_L(L)
        self.refresh()

    def set_T(self, T):
        if T > 0:
            self._T = dt.timedelta(hours=T)

    def commit(self):
        """Save the current scenario state to the undo history.

        Returns:
            None: Stores deep copies of the scenario state and clears redo history.
        """
        self.undo_queue.append((copy.deepcopy(self._AVL),
                                copy.deepcopy(self._BST),
                                copy.deepcopy(self.reports_queue),
                                copy.deepcopy(self._eliminated_ids),
                                copy.deepcopy(self._archived_trees)))
        self.redo_queue.clear()

    def undo(self) -> Scenario:
        """Restore the previous scenario state.

        Returns:
            Scenario: The scenario after undoing the most recent change.
        """
        self.redo_queue.append((copy.deepcopy(self._AVL),
                                copy.deepcopy(self._BST),
                                copy.deepcopy(self.reports_queue),
                                copy.deepcopy(self._eliminated_ids),
                                copy.deepcopy(self._archived_trees)))
        (self._AVL, self._BST, self.reports_queue, self._eliminated_ids,
         self._archived_trees) = self.undo_queue.pop()
        self.refresh()

    def redo(self) -> Scenario:
        """Restore a state removed by an undo operation.

        Returns:
            Scenario: The scenario after redoing the most recent undone change.
        """
        self.undo_queue.append((copy.deepcopy(self._AVL),
                                copy.deepcopy(self._BST),
                                copy.deepcopy(self.reports_queue),
                                copy.deepcopy(self._eliminated_ids),
                                copy.deepcopy(self._archived_trees)))
        (self._AVL, self._BST, self.reports_queue, self._eliminated_ids,
         self._archived_trees) = self.redo_queue.pop()
        self.refresh()

    @property
    def can_undo(self):
        """Indicate whether an undo operation is available.

        Returns:
            bool: True when the undo queue is not empty.
        """
        return len(self.undo_queue) > 0

    @property
    def can_redo(self):
        """Indicate whether a redo operation is available.

        Returns:
            bool: True when the redo queue is not empty.
        """
        return len(self.redo_queue) > 0

    @EventTrigger
    def refresh(self):
        """Refresh scenario-dependent state after a mutation.

        Returns:
            None: Triggers the event refresh callback.
        """
        pass