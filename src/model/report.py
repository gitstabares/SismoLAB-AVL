"""Seismic report model and validation logic.

This module defines :class:`Report`, which stores and validates information
about a seismic event before it is processed or persisted.
"""

import stat

from numpy import isin

from .point import Point
from .key import Key
from datetime import datetime as dt


class Report:
    """Represents a seismic report entry.

    The class validates the incoming values and keeps the report data in a
    normalized form suitable for further processing or persistence.
    """

    def __init__(
            self,
            identifier:int,
            magnitude:float,
            deepness:float,
            x:float,
            y:float,
            date:str,
            station:str = "",
            is_populated:bool = False,
            review:int = 1):

        """Initialize a report with the provided seismic information.

        Args:
            id (int): Unique report identifier.
            magnitude (float): Seismic magnitude of the event.
            deepness (float): Depth of the earthquake in kilometers.
            x (float): X coordinate of the epicenter.
            y (float): Y coordinate of the epicenter.
            date (str): ISO date string for the event date/time.
            station (str): Station that generated or reported the event.
            review (int, optional): Review score or level associated with the report. Defaults to 1.
        """
        self.set_identifier(identifier)
        self.set_magnitude(magnitude)
        self.set_deepness(deepness)
        self.set_epicenter(x,y)
        self.set_date(date)
        self.set_station(station)
        self.set_is_populated(is_populated)
        self.set_review(review)
        self.set_key(Key(self.get_magnitude(),
                        self.get_deepness(),
                        self.get_is_populated(),
                        self.get_identifier()))

    def __repr__(self) -> str:
        """Return the report key as its string representation.

        Returns:
            str: The report key.
        """
        return f"{self.get_key()}"

    def get_priority(self):
        """Return the priority value calculated from the report key.

        Returns:
            Any: The priority value associated with the report.
        """
        return self._key.get_priority()

    def get_identifier(self) -> int:
        """Return the report identifier.

        Returns:
            int: The unique report ID.
        """
        return self._identifier

    def set_identifier(self, identifier:int):
        """Validate and set the report identifier.

        Args:
            identifier (Any): The ID to set.

        Raises:
            ValueError: If the ID is not between 1 and 999999.
        """
        if identifier is None:
            raise Exception("Identifier can't be none")
        identifier = int(identifier)
        if not (1 <= identifier <= 999999):
            raise ValueError(f"Id must be an integer between 1 and 999999. Got: {identifier}")
        self._identifier = identifier

    def get_magnitude(self) -> float:
        """Return the earthquake magnitude.

        Returns:
            float: The magnitude.
        """
        return self._magnitude

    def set_magnitude(self, magnitude:float):
        """Validate and set the magnitude range and one decimal place.

        Args:
            magnitude (float): The magnitude to set.

        Raises:
            ValueError: If the magnitude is not between -2 and 10.
        """
        if magnitude is None:
            raise Exception("Magnitude can't be none")
        if not (-2 <= magnitude <= 10):
            raise ValueError(f"Magnitude must be between -2 and 10. Got: {magnitude}")
        self._magnitude = magnitude

    def get_deepness(self) -> float:
        """Return the earthquake depth in kilometers.

        Returns:
            float: The depth.
        """
        return self._deepness

    def set_deepness(self, deepness:float):
        """Validate and set the depth range and one decimal place.

        Args:
            deepness (float): The depth to set.

        Raises:
            ValueError: If the depth is not between 0 and 700.
        """
        if deepness is None:
            raise Exception("Deepness can't be none")
        if not (0 <= deepness <= 700):
            raise ValueError(f"Deepness must be between 0 and 700. Got: {deepness}")
        self._deepness = deepness

    def get_epicenter(self) -> Point:
        """Return the epicenter point.

        Returns:
            Point: The epicenter coordinates.
        """
        return self._epicenter

    def set_epicenter(self, x:float, y:float):
        """Create and set a Point object for the epicenter coordinates.

        Args:
            point (Point): The point representing the epicenter.
        """
        if not (0 <= x <= 1000) or not (0 <= y <= 1000):
            raise ValueError(f"Deepness must be between 0 and 700. Got: ({x},{y})")
        self._epicenter = Point(x,y)

    def get_date(self) -> dt:
        """Return the event date as a datetime object.

        Returns:
            dt: The event date.
        """
        return self._date

    def set_date(self, date:str):
        """Parse and set the ISO date string into a datetime object.

        Args:
            date (str): The ISO format date string.
        """
        self._date = dt.fromisoformat(date)

    def get_station(self) -> str:
        """Return the station that originated the report.

        Returns:
            str: The origin station string.
        """
        return self._station

    def set_station(self, station:str):
        """Set the station name.

        Args:
            station (str): The station name.
        """
        self._station = station

    def get_is_populated(self) -> bool:
        """Return whether the report has population data.

        Returns:
            bool: True if the report is populated; otherwise, False.
        """
        return self._is_populated

    def set_is_populated(self, is_populated:bool):
        """Set the populated-state flag for the report.

        Args:
            is_populated (bool): Whether the report contains population data.
        """
        self._is_populated = is_populated

    def get_review(self) -> int:
        """Return the review value associated with the report.

        Returns:
            int: The review value.
        """
        return self._review

    def set_review(self, review:int):
        """Validate and set the review value and ensure it is not negative.

        Args:
            review (Any): The review value to set.

        Raises:
            ValueError: If the review is negative.
        """
        if review is None:
            raise Exception("Review can't be none")
        review = int(review)
        if review < 0:
            raise ValueError(f"Review must be non-negative. Got: {review}")
        self._review = review

    def get_key(self) -> Key:
        return self._key

    def set_key(self, key:Key):
        self._key = key