from collections import deque
from .scenario import Scenario
from src.utils import copy


class ScenarioManager:
    def __init__(self, initial_scenario:Scenario):
        self._current_scenario = initial_scenario
        self._undo_stack = deque(maxlen=3)
        self._redo_stack = deque(maxlen=3)

    def commit(self, new_scenario:Scenario):
        self._undo_stack.append(self._current_scenario)
        self._current_scenario = new_scenario
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return False
        self._redo_stack.append(self._current_scenario)
        self._current_scenario = self._undo_stack.pop()
        return True

    def redo(self):
        if not self._redo_stack:
            return False
        self._undo_stack.append(self._current_scenario)
        self._current_scenario = self._redo_stack.pop()
        return True