from src.core import *


class Event(Node):
    """Represents a seismic event with its metadata and impact information.

    The object inherits from Node and uses a Key generated from the event's
    magnitude, deepness, population flag, and identifier to support ordered
    storage or lookup in the data structure.
    """

    def __init__(self, report, is_populated):
        """Initialize an event with the given seismic data.

        Args:
            report (Any): The report object containing seismic data.
            is_populated (bool): Indicates if the event occurred in a populated area.
        """
        super().__init__(Key(report.get_magnitude(), report.get_deepness(), is_populated, report.get_id()))
        self.__id = report.get_id()
        self.__magnitude = report.get_magnitude()
        self.__deepness = report.get_deepness()
        self.__epicenter = report.get_epicenter()
        self.__date = report.get_date()
        self.__review = report.get_review()
        self.__origin_station = report.get_origin_station()
        self.__is_populated = is_populated
        self.__revised = False
        self.__aftershocks = []
        self.__costly_access = False

    def set_all(self, event):
        """Set all event attributes from another event object.

        Args:
            event (Any): Another event object to copy data from.
        """
        self.set_magnitude(event.get_magnitude())
        self.set_deepness(event.get_deepness())
        self.set_epicenter(event.get_epicenter())
        self.set_date(event.get_date())
        self.set_review(event.get_review())
        self.set_origin_station(event.get_origin_station())
        self.set_is_populated(event.get_is_populated())
        self.update_key()

    def get_all(self):
        """Return all attributes of the event as a tuple.

        Returns:
            Tuple[Any, float, float, Any, Any, int, Any, bool]: A tuple containing
                id, magnitude, deepness, epicenter, date, review, origin_station, and is_populated.
        """
        return (
            self.__id,
            self.__magnitude,
            self.__deepness,
            self.__epicenter,
            self.__date,
            self.__review,
            self.__origin_station,
            self.__is_populated
        )

    def update_key(self):
        """Refresh the key after any attribute affecting the key changes."""
        self.set_key(Key(self.__magnitude, self.__deepness, self.__is_populated, self.__id))

    def get_id(self):
        """Return the event identifier.

        Returns:
            Any: The identifier of the event.
        """
        return self.__id

    def get_magnitude(self):
        """Return the earthquake magnitude.

        Returns:
            float: The magnitude of the event.
        """
        return self.__magnitude

    def set_magnitude(self, magnitude):
        """Set a new magnitude and update the related key.

        Args:
            magnitude (float): The new magnitude value.
        """
        self.__magnitude = magnitude
        self.update_key()

    def get_deepness(self):
        """Return the earthquake depth.

        Returns:
            float: The deepness of the event.
        """
        return self.__deepness

    def set_deepness(self, deepness):
        """Set a new deepness value.

        Args:
            deepness (float): The new deepness value.
        """
        self.__deepness = deepness
        self.update_key()

    def get_epicenter(self):
        """Return the epicenter location.

        Returns:
            Any: The epicenter of the event.
        """
        return self.__epicenter

    def set_epicenter(self, epicenter):
        """Set a new epicenter value.

        Args:
            epicenter (Any): The new epicenter value.
        """
        self.__epicenter = epicenter

    def get_date(self):
        """Return the date of the event.

        Returns:
            Any: The date of the event.
        """
        return self.__date

    def set_date(self, date):
        """Set the event date.

        Args:
            date (Any): The new date value.
        """
        self.__date = date

    def get_review(self):
        """Return the review score associated with the event.

        Returns:
            int: The review score.
        """
        return self.__review

    def set_review(self, review):
        """Set the review value, coercing it to an integer.

        Args:
            review (Any): The review value to set.
        """
        self.__review = int(review)

    def get_origin_station(self):
        """Return the station that reported the event.

        Returns:
            Any: The origin station.
        """
        return self.__origin_station

    def set_origin_station(self, origin_station):
        """Set the origin station for the event.

        Args:
            origin_station (Any): The new origin station.
        """
        self.__origin_station = origin_station

    def get_is_populated(self):
        """Return whether the event occurred in a populated area.

        Returns:
            bool: True if populated, False otherwise.
        """
        return self.__is_populated

    def set_is_populated(self, value):
        """Set whether the event occurred in a populated area.

        Args:
            value (bool): The new population status.
        """
        self.__is_populated = value
        self.update_key()

    def get_revised(self):
        """Return whether the event has been revised.

        Returns:
            bool: True if revised, False otherwise.
        """
        return self.__revised

    def set_revised(self, revised):
        """Set the revised status.

        Args:
            revised (bool): The new revised status.
        """
        self.__revised = revised

    def get_costly_access(self):
        """Return whether access to this event is considered costly.

        Returns:
            bool: True if costly access, False otherwise.
        """
        return self.__costly_access

    def set_costly_access(self, costly_access):
        """Set the costly-access flag.

        Args:
            costly_access (bool): The new costly-access status.
        """
        self.__costly_access = costly_access

    def get_aftershocks(self):
        """Return the list of aftershocks associated with this event.

        Returns:
            List[Any]: A list of aftershock events.
        """
        return self.__aftershocks

    def set_aftershocks(self, value):
        """Return the list of aftershocks associated with this event.

        Returns:
            List[Any]: A list of aftershock events.
        """
        self.__aftershocks = value