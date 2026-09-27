"""Model representation of a seismic event.

This module defines the Event class, which stores the data for an earthquake
record and exposes the accessors used by the rest of the application.
"""

from src.model import Key
from src.model import Node


class Event(Node):
    """Represents a seismic event with its metadata and impact information.

    The object inherits from Node and uses a Key generated from the event's
    magnitude, deepness, population flag, and identifier to support ordered
    storage or lookup in the data structure.
    """

    def __init__(
        self,
        id,
        magnitude,
        deepness,
        epicenter,
        date,
        review,
        origin_station,
        revised,
        is_populated
    ):
        """Initialize an event with the given seismic data.

        Args:
            id: Unique identifier of the event.
            magnitude: Earthquake magnitude value.
            deepness: Depth of the earthquake source.
            epicenter: Geographic epicenter name or location.
            date: Date of occurrence.
            review: Evaluation score or review metric.
            origin_station: Station that originated the report.
            revised: Whether the report has been revised.
            is_populated: Indicates if the event occurred in a populated area.
        """
        super().__init__(Key(magnitude, deepness, is_populated, id))
        self.__id = id
        self.__magnitude = magnitude
        self.__deepness = deepness
        self.__epicenter = epicenter
        self.__date = date
        self.__review = review
        self.__origin_station = origin_station
        self.__revised = revised
        self.__is_populated = is_populated
        self.__aftershocks = []
        self.__costly_access = False

    def get_key(self):
        """Return the event key used to compare or index this node."""
        return self.__key

    def update_key(self):
        """Refresh the key after any attribute affecting the key changes."""
        self.__key = Key(self.__magnitude, self.__deepness, self.__is_populated, self.__id)

    def get_id(self):
        """Return the event identifier."""
        return self.__id

    def get_magnitude(self):
        """Return the earthquake magnitude."""
        return self.__magnitude

    def set_magnitude(self, magnitude):
        """Set a new magnitude and update the related key."""
        self.__magnitude = magnitude

    def get_deepness(self):
        """Return the earthquake depth."""
        return self.__deepness

    def set_deepness(self, deepness):
        """Set a new deepness value."""
        self.__deepness = deepness

    def get_epicenter(self):
        """Return the epicenter location."""
        return self.__epicenter

    def set_epicenter(self, epicenter):
        """Set a new epicenter value."""
        self.__epicenter = epicenter

    def get_date(self):
        """Return the date of the event."""
        return self.__date

    def set_date(self, date):
        """Set the event date."""
        self.__date = date

    def get_review(self):
        """Return the review score associated with the event."""
        return self.__review

    def set_review(self, review):
        """Set the review value, coercing it to an integer."""
        self.__review = int(review)

    def get_origin_station(self):
        """Return the station that reported the event."""
        return self.__origin_station

    def set_origin_station(self, origin_station):
        """Set the origin station for the event."""
        self.__origin_station = origin_station

    def get_revised(self):
        """Return whether the event has been revised."""
        return self.__revised

    def set_revised(self, revised):
        """Set the revised status."""
        self.__revised = revised

    def get_costly_access(self):
        """Return whether access to this event is considered costly."""
        return self.__costly_access

    def set_costly_access(self, costly_access):
        """Set the costly-access flag."""
        self.__costly_access = costly_access

    def get_aftershocks(self):
        """Return the list of aftershocks associated with this event."""
        return self.__aftershocks

    # Notes:
    # - The class intentionally stores all attributes as private fields.
    # - Aftershock data is kept as a list and can be extended by other modules.
    # - A review is converted to int to normalize the data type for storage.
