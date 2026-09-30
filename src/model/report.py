from .point import Point
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
        self.__set_id(id)
        self.__set_magnitude(magnitude)
        self.__set_deepness(deepness)
        self.__set_epicenter(x, y)
        self.__set_date(date)
        self.__set_review(review)
        self.__origin_station = origin_station

    def get_id(self):
        """Return the report identifier."""
        return self.__id

    def __set_id(self, id):
        """Validate the report identifier."""
        val = int(id)
        if not (1 <= val <= 999999):
            raise ValueError(f"id must be between 1 and 999999. Got: {val}")
        self.__id = val

    def get_magnitude(self):
        """Return the earthquake magnitude."""
        return self.__magnitude

    def __set_magnitude(self, magnitude):
        """Validate the magnitude range and one decimal place."""
        val = round(magnitude, 1)
        if not (-2 <= val <= 10):
            raise ValueError(f"magnitude must be between -2 and 10. Got: {val}")
        self.__magnitude = val

    def get_deepness(self):
        """Return the earthquake depth in kilometers."""
        return self.__deepness

    def __set_deepness(self, deepness):
        """Validate the depth range and one decimal place."""
        val = round(deepness, 1)
        if not (0 <= val <= 700):
            raise ValueError(f"deepness must be between 0 and 700. Got: {val}")
        self.__deepness = val

    def get_epicenter(self):
        """Return the epicenter point."""
        return self.__epicenter

    def __set_epicenter(self, x, y):
        """Create a Point object for the epicenter coordinates"""
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
        val = int(review)
        if val < 0:
            raise ValueError(f"review must be non-negative. Got: {val}")
        self.__review = val

    def get_origin_station(self):
        """Return the station that originated the report."""
        return self.__origin_station