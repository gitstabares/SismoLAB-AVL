class Key(tuple):
    """Represents a key used for prioritizing and ordering seismic events.

    The priority is determined by the magnitude, deepness, and whether the area is populated.
    Higher priority indicates a more critical event.
    """

    def __new__(cls, magnitude:float, deepness:float, is_populated:bool, identifier:int):
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
        return super().__new__(cls, [priority, magnitude, identifier])

    @property
    def priority(self) -> int:
        return self[0]

    @property
    def magnitude(self) -> float:
        return self[1]

    @property
    def identifier(self) -> float:
        return self[2]

    def __eq__(self, other:Key):
        """Checks if two Key instances are equal based on their identifier.

        Args:
            other (Any): The other Key instance to compare with.

        Returns:
            bool: True if the identifiers are equal, False otherwise.
        """
        return self.identifier == other.identifier

    def __ne__(self, other:Key):
        return (self.priority != other.priority 
                or self.magnitude != other.magnitude 
                or self.identifier != other.identifier)

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
        if self.priority != other.priority:
            return self.priority < other.priority

        if self.magnitude != other.magnitude:
            return self.magnitude < other.magnitude

        return self.identifier < other.identifier

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
        if self.priority != other.priority:
            return self.priority > other.priority

        if self.magnitude != other.magnitude:
            return self.magnitude > other.magnitude

        return self.identifier > other.identifier

    def __repr__(self):
        """Returns a string representation of the Key.

        Returns:
            str: A string in the format "(priority, magnitude, SIS-identifier)".
        """
        return f"({self.priority}, {self.magnitude}, SIS-{self.identifier:06d})"
