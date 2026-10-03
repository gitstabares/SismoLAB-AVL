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

        Report.__init__(self,
                        report.identifier,
                        report.magnitude,
                        report.deepness,
                        report.epicenter.x,
                        report.epicenter.y,
                        report.date,
                        report.station,
                        report.is_populated,
                        report.review)
        Node.__init__(self, Key(self.magnitude, self.deepness, self.is_populated, self.identifier))
        self.revised = False
        self.aftershocks = []
        self.costly_access = False

    @property
    def revised(self) -> bool:
        return self.__revised

    @revised.setter
    def revised(self, revised:bool):
        self.__revised = revised

    @property
    def aftershocks(self) -> list:
        return self.__aftershocks

    @aftershocks.setter
    def aftershocks(self, aftershocks:list):
        self.__aftershocks = aftershocks

    @property
    def costly_access(self) -> bool:
        return self.__costly_access

    @costly_access.setter
    def costly_access(self, costly_access:bool):
        self.__costly_access = costly_access

    @Report.magnitude.setter
    def magnitude(self, magnitude):
        Report.magnitude.fset(self, magnitude)
        self.update_key()

    @Report.deepness.setter
    def deepness(self, deepness):
        Report.deepness.fset(self, deepness)
        self.update_key()

    @Report.is_populated.setter
    def is_populated(self, is_populated):
        Report.is_populated.fset(self, is_populated)
        self.update_key()

    def set_data(self, report:Report):
        """Set all event attributes from a report object.

        Args:
            report (Any): A report object to get data from.
        """
        self.__dict__.update(report.__dict__)
        self.update_key()

    def get_data(self) -> dict:
        notatr = ('_Event__key','_Event__revised','_Event__aftershocks','_Event__costly_access','__dict__')
        return {k: v for k, v in self.__dict__.items() if k not in notatr}

    def update_key(self):
        self.key = Key(self.magnitude, self.deepness, self.is_populated, self.identifier)