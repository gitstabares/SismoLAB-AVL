from .node import Node
from .report import Report
from .key import Key


class Event(Node, Report):
    """Represents a seismic event with its metadata and impact information.

    The object inherits from Node and uses a Key generated from the event's
    magnitude, deepness, population flag, and identifier to support ordered
    storage or lookup in the data structure.
    """

    def __init__(self, report:Report):
        """Initialize an event with the given seismic data.

        Args:
            report (Any): The report object containing seismic data.
        """

        self._identifier = report.get_identifier()
        self._magnitude = report.get_magnitude()
        self._deepness = report.get_deepness()
        self._epicenter = report.get_epicenter()
        self._date = report.get_date()
        self._station = report.get_station()
        self._is_populated = report.get_is_populated()
        self._review = report.get_review()
        Node.__init__(self, Key(report.get_magnitude(), report.get_deepness(), report.get_is_populated(), self.get_identifier()))
        self.set_revised(False)
        self.set_aftershocks([])
        self.set_costly_access(False)

    def get_revised(self) -> bool:
        return self._revised

    def set_revised(self, revised: bool):
        self._revised = revised

    def get_aftershocks(self) -> list:
        return self._aftershocks

    def set_aftershocks(self, aftershocks: list):
        self._aftershocks = aftershocks

    def get_costly_access(self) -> bool:
        return self._costly_access

    def set_costly_access(self, costly_access: bool):
        self._costly_access = costly_access

    def set_magnitude(self, magnitude):
        Report.set_magnitude(self,magnitude)
        self.update_key()

    def set_deepness(self, deepness):
        Report.set_deepness(self,deepness)
        self.update_key()

    def set_is_populated(self, is_populated):
        Report.set_is_populated(self,is_populated)
        self.update_key()

    def set_data(self, report:Report):
        """Set all event attributes from a report object.

        Args:
            report (Any): A report object to get data from.
        """
        self.__dict__.update(report.__dict__)
        self.update_key()

    def get_data(self) -> dict:
        notatr = ('_Event_key','_Event_revised','_Event_aftershocks','_Event_costly_access')
        return {k: v for k, v in self.__dict__.items() if k not in notatr}

    def update_key(self):
        self.set_key(Key(self.get_magnitude(), self.get_deepness(), self.get_is_populated(), self.get_identifier()))