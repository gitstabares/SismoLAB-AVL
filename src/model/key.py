class Key():
    """Represents a key used for prioritizing and ordering seismic events.

    The priority is determined by the magnitude, deepness, and whether the area is populated.
    Higher priority indicates a more critical event.
    """

    def __init__(self, magnitude:float, deepness:float, is_populated:bool, identifier:int):
        """Initializes a Key instance.

        Args:
            magnitude (float): The magnitude of the seismic event.
            deepness (float): The depth of the seismic event in kilometers.
            is_populated (bool): True if the event occurred in a populated area.
            identifier (Any): A unique identifier for the event.
        """
        if magnitude >= 4.5:
            if magnitude >= 6.0 or (deepness <= 30 and is_populated):
                priority = 3
            else:
                priority = 2
        else:
            priority = 1
        self._priority = priority
        self._magnitude = magnitude
        self._identifier = identifier

    def get_priority(self) -> int:
        return self._priority

    def get_magnitude(self) -> float:
        return self._magnitude

    def get_identifier(self) -> float:
        return self._identifier

    def __eq__(self, other:Key):
        """Checks if two Key instances are equal based on their identifier.

        Args:
            other (Any): The other Key instance to compare with.

        Returns:
            bool: True if the identifiers are equal, False otherwise.
        """
        return self.get_identifier() == other.get_identifier()

    def __ne__(self, other:Key):
        return (self.get_priority() != other.get_priority() 
                or self.get_magnitude() != other.get_magnitude() 
                or self.get_identifier() != other.get_identifier())

    def __lt__(self, other:Key):
        """Determines if this Key is less than another Key.

        Comparison is done in the following order:
        1. Priority
        2. Magnitude
        3. identifier

        Args:
            other (Any): The other Key instance to compare with.

        Returns:
            bool: True if this Key is strictly less than the other Key.
        """
        if self.get_priority() != other.get_priority():
            return self.get_priority() < other.get_priority()

        if self.get_magnitude() != other.get_magnitude():
            return self.get_magnitude() < other.get_magnitude()

        return self.get_identifier() < other.get_identifier()

    def __gt__(self, other:Key):
        """Determines if this Key is greater than another Key.

        Comparison is done in the following order:
        1. Priority
        2. Magnitude
        3. identifier

        Args:
            other (Any): The other Key instance to compare with.

        Returns:
            bool: True if this Key is strictly greater than the other Key.
        """
        if self.get_priority() != other.get_priority():
            return self.get_priority() > other.get_priority()

        if self.get_magnitude() != other.get_magnitude():
            return self.get_magnitude() > other.get_magnitude()

        return self.get_identifier() > other.get_identifier()

    def __repr__(self):
        """Returns a string representation of the Key.

        Returns:
            str: A string in the format "(priority, magnitude, SIS-identifier)".
        """
        return f"(P={self.get_priority()}, M={self.get_magnitude()}, SIS-{self.get_identifier():06d})"
