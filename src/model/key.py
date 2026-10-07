class Key():
    """Represents a seismic event priority key.

    The priority combines the event magnitude, depth, and whether the event
    occurred in a populated area. A higher priority indicates a more critical
    event.
    """

    def __init__(self, magnitude: float, deepness: float, is_populated: bool, identifier: int):
        """Initialize a key for a seismic event.

        Args:
            magnitude (float): The magnitude of the seismic event.
            deepness (float): The depth of the seismic event in kilometers.
            is_populated (bool): True if the event occurred in a populated area.
            identifier (int): A unique identifier for the event.
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
        """Return the priority assigned to the seismic event.

        Returns:
            int: The event priority, where a larger value indicates greater
                urgency.
        """
        return self._priority

    def get_magnitude(self) -> float:
        """Return the seismic event magnitude.

        Returns:
            float: The magnitude of the seismic event.
        """
        return self._magnitude

    def get_identifier(self) -> float:
        """Return the event identifier.

        Returns:
            float: The identifier associated with the event.
        """
        return self._identifier

    def __eq__(self, other: Key):
        """Return whether this key is equal to another value.

        The comparison is based on the event identifier. If ``other`` is not a
        ``Key`` instance, the comparison is performed against ``other`` as an
        identifier value.

        Args:
            other (Key | Any): The value to compare with this key.

        Returns:
            bool: True if the identifiers are equal; otherwise, False.
        """
        if not isinstance(other, Key):
            return self.get_identifier() == other
        return self.get_identifier() == other.get_identifier()

    def __ne__(self, other: Key):
        """Return whether this key is not equal to another key.

        Args:
            other (Key): The key to compare with this key.

        Returns:
            bool: True if the priority, magnitude, or identifier differs;
                otherwise, False.
        """
        return (self.get_priority() != other.get_priority()
                or self.get_magnitude() != other.get_magnitude()
                or self.get_identifier() != other.get_identifier())

    def __lt__(self, other: Key):
        """Return whether this key has a lower order than another key.

        Keys are ordered by priority, then magnitude, and finally identifier.

        Args:
            other (Key): The key to compare with this key.

        Returns:
            bool: True if this key is strictly less than ``other``; otherwise,
                False.
        """
        if self.get_priority() != other.get_priority():
            return self.get_priority() < other.get_priority()

        if self.get_magnitude() != other.get_magnitude():
            return self.get_magnitude() < other.get_magnitude()

        return self.get_identifier() < other.get_identifier()

    def __gt__(self, other: Key):
        """Return whether this key has a greater order than another key.

        Keys are ordered by priority, then magnitude, and finally identifier.

        Args:
            other (Key): The key to compare with this key.

        Returns:
            bool: True if this key is strictly greater than ``other``;
                otherwise, False.
        """
        if self.get_priority() != other.get_priority():
            return self.get_priority() > other.get_priority()

        if self.get_magnitude() != other.get_magnitude():
            return self.get_magnitude() > other.get_magnitude()

        return self.get_identifier() > other.get_identifier()

    def __repr__(self):
        """Return a printable representation of the key.

        Returns:
            str: A string in the format
                ``(P=<priority>, M=<magnitude>, SIS-<identifier>)``.
        """
        return f"(P={self.get_priority()}, M={self.get_magnitude()}, SIS-{self.get_identifier():06d})"
