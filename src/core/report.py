from .point import Point
from datetime import datetime as dt

class Report:
    """Represents a seismic report entry.

    The class validates the incoming values and keeps the report data in a
    normalized form suitable for further processing or persistence.
    """

    def __init__(self, identifier, magnitude, deepness, x, y, date, station, review = 1):
        """Initialize a report with the provided seismic information.

        Args:
            id (int): Unique report identifier.
            magnitude (float): Seismic magnitude of the event.
            deepness (float): Depth of the earthquake in kilometers.
            x (float): X coordinate of the epicenter.
            y (float): Y coordinate of the epicenter.
            date (str): ISO date string for the event date/time.
            origin_station (str): Station that generated or reported the event.
            review (int, optional): Review score or level associated with the report. Defaults to 1.
        """
        self.__set_id(identifier)
        self.__set_magnitude(magnitude)
        self.__set_deepness(deepness)
        self.__set_epicenter(x, y)
        self.__set_date(date)
        self.__set_review(review)
        self.__origin_station = station

    def get_id(self):
        """Return the report identifier.

        Returns:
            int: The unique report ID.
        """
        return self.__id

    def __set_id(self, id):
        """Validate and set the report identifier.

        Args:
            id (Any): The ID to set.

        Raises:
            ValueError: If the ID is not between 1 and 999999.
        """
        val = int(id)
        if not (1 <= val <= 999999):
            raise ValueError(f"Id must be between 1 and 999999. Got: {val}")
        self.__id = val

    def get_magnitude(self):
        """Return the earthquake magnitude.

        Returns:
            float: The magnitude.
        """
        return self.__magnitude

    def __set_magnitude(self, magnitude):
        """Validate and set the magnitude range and one decimal place.

        Args:
            magnitude (float): The magnitude to set.

        Raises:
            ValueError: If the magnitude is not between -2 and 10.
        """
        val = round(magnitude, 1)
        if not (-2 <= val <= 10):
            raise ValueError(f"Magnitude must be between -2 and 10. Got: {val}")
        self.__magnitude = val

    def get_deepness(self):
        """Return the earthquake depth in kilometers.

        Returns:
            float: The depth.
        """
        return self.__deepness

    def __set_deepness(self, deepness):
        """Validate and set the depth range and one decimal place.

        Args:
            deepness (float): The depth to set.

        Raises:
            ValueError: If the depth is not between 0 and 700.
        """
        val = round(deepness, 1)
        if not (0 <= val <= 700):
            raise ValueError(f"Deepness must be between 0 and 700. Got: {val}")
        self.__deepness = val

    def get_epicenter(self):
        """Return the epicenter point.

        Returns:
            Point: The epicenter coordinates.
        """
        return self.__epicenter

    def __set_epicenter(self, x, y):
        """Create and set a Point object for the epicenter coordinates.

        Args:
            x (float): The X coordinate.
            y (float): The Y coordinate.
        """
        self.__epicenter = Point(x, y)

    def get_date(self):
        """Return the event date as a datetime object.

        Returns:
            dt: The event date.
        """
        return self.__date

    def __set_date(self, date):
        """Parse and set the ISO date string into a datetime object.

        Args:
            date (str): The ISO format date string.
        """
        self.__date = dt.fromisoformat(date)

    def get_review(self):
        """Return the review value associated with the report.

        Returns:
            int: The review value.
        """
        return self.__review

    def __set_review(self, review):
        """Validate and set the review value and ensure it is not negative.

        Args:
            review (Any): The review value to set.

        Raises:
            ValueError: If the review is negative.
        """
        val = int(review)
        if val < 0:
            raise ValueError(f"Review must be non-negative. Got: {val}")
        self.__review = val

    def get_origin_station(self):
        """Return the station that originated the report.

        Returns:
            str: The origin station string.
        """
        return self.__origin_station