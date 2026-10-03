from .point import Point
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
        
        self.identifier = identifier
        self.magnitude = magnitude
        self.deepness = deepness
        self.epicenter = Point(x,y)
        self.date = date
        self.station = station
        self.is_populated = is_populated
        self.review = review

    @property
    def identifier(self) -> int:
        """Return the report identifier.

        Returns:
            int: The unique report ID.
        """
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier:int):
        """Validate and set the report identifier.

        Args:
            identifier (Any): The ID to set.

        Raises:
            ValueError: If the ID is not between 1 and 999999.
        """

        val = int(identifier)
        if not (1 <= val <= 999999):
            raise ValueError(f"Id must be an integer between 1 and 999999. Got: {val}")
        self.__identifier = val

    @property
    def magnitude(self) -> float:
        """Return the earthquake magnitude.

        Returns:
            float: The magnitude.
        """
        return self.__magnitude

    @magnitude.setter
    def magnitude(self, magnitude:float):
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

    @property
    def deepness(self) -> float:
        """Return the earthquake depth in kilometers.

        Returns:
            float: The depth.
        """
        return self.__deepness

    @deepness.setter
    def deepness(self, deepness:float):
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

    @property
    def epicenter(self) -> Point:
        """Return the epicenter point.

        Returns:
            Point: The epicenter coordinates.
        """
        return self.__epicenter

    @epicenter.setter
    def epicenter(self, point:Point):
        """Create and set a Point object for the epicenter coordinates.

        Args:
            x (float): The X coordinate.
            y (float): The Y coordinate.
        """
        if not (0 <= point.x <= 1000) or not (0 <= point.y <= 1000):
            raise ValueError(f"Deepness must be between 0 and 700. Got: {point}")
        self.__epicenter = point

    @property
    def date(self) -> dt:
        """Return the event date as a datetime object.

        Returns:
            dt: The event date.
        """
        return self.__date

    @date.setter
    def date(self, date:str):
        """Parse and set the ISO date string into a datetime object.

        Args:
            date (str): The ISO format date string.
        """
        self.__date = dt.fromisoformat(date)

    @property
    def review(self) -> int:
        """Return the review value associated with the report.

        Returns:
            int: The review value.
        """
        return self.__review

    @review.setter
    def review(self, review:int):
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

    @property
    def station(self) -> str:
        """Return the station that originated the report.

        Returns:
            str: The origin station string.
        """
        return self.__station

    @station.setter
    def station(self, station:str):
        """Set the station name.

        Args:
            station (str): The station name.
        """
        self.__station = station

    @property
    def is_populated(self) -> bool:
        return self.__is_populated

    @is_populated.setter
    def is_populated(self, is_populated:bool):
        self.__is_populated = is_populated