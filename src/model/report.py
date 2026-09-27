"""Model for seismic report data.

This module defines the Report entity used to store and validate information
about a seismic event, including its identifier, magnitude, depth, epicenter,
date, review status, and the station from which the report originated.
"""

from src.model import Point
from datetime import datetime as dt


class Report:
    """Represents a seismic report entry.

    The class validates the incoming values and keeps the report data in a
    normalized form suitable for further processing or persistence.
    """

    def __init__(self, id, magnitude, deepness, x, y, date, review, origin_station):
        """Initialize a report with the provided seismic information.

        Args:
            id: Unique report identifier.
            magnitude: Seismic magnitude of the event.
            deepness: Depth of the earthquake in kilometers.
            x: X coordinate of the epicenter.
            y: Y coordinate of the epicenter.
            date: ISO date string for the event date/time.
            review: Review score or level associated with the report.
            origin_station: Station that generated or reported the event.
        """
        self.__id = self.__set_id(id)
        self.__magnitude = self.__set_magnitude(magnitude)
        self.__deepness = self.__set_deepness(deepness)
        self.__epicenter = self.__set_epicenter(x, y)
        self.__date = self.__set_date(date)
        self.__review = self.__set_review(review)
        self.__origin_station = origin_station

    def get_id(self):
        """Return the report identifier."""
        return self.__id

    def __set_id(self, id):
        """Validate and clamp the report identifier."""
        self.__id = max(1, min(999999, int(id)))

    def get_magnitude(self):
        """Return the earthquake magnitude."""
        return self.__magnitude

    def __set_magnitude(self, magnitude):
        """Normalize the magnitude to a valid range and one decimal place."""
        self.__magnitude = max(-2, min(10, round(magnitude, 1)))

    def get_deepness(self):
        """Return the earthquake depth in kilometers."""
        return self.__deepness

    def __set_deepness(self, deepness):
        """Normalize the depth to a valid range and one decimal place."""
        self.__deepness = max(0, min(700, round(deepness, 1)))

    def get_epicenter(self):
        """Return the epicenter point."""
        return self.__epicenter

    def __set_epicenter(self, x, y):
        """Create a Point object for the epicenter coordinates."""
        self.__epicenter = Point(x, y)

    def get_date(self):
        """Return the event date as a datetime object."""
        return self.__date

    def __set_date(self, date):
        """Parse the ISO date string into a datetime object."""
        self.__date = dt.fromisoformat(date)

    def get_review(self):
        """Return the review value associated with the report."""
        return self.__review

    def __set_review(self, review):
        """Validate the review value and ensure it is not negative."""
        self.__review = max(0, int(review))

    def get_origin_station(self):
        """Return the station that originated the report."""
        return self.__origin_station
    


