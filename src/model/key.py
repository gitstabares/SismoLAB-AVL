class Key:
    """
    Represents a key used for prioritizing and ordering seismic events.

    The priority is determined by the magnitude, deepness, and whether the area is populated.
    Higher priority indicates a more critical event.
    """

    def __init__(self, magnitude, deepness, is_populated, id):
        """
        Initializes a Key instance.

        Args:
            magnitude (float): The magnitude of the seismic event.
            deepness (float): The depth of the seismic event in kilometers.
            is_populated (bool): True if the event occurred in a populated area, False otherwise.
            id (int/str): A unique identifier for the event.
        """
        if magnitude >= 4.5:
            if magnitude >= 6.0 or (deepness <= 30 and is_populated):
                self.__priority = 3
            else:
                self.__priority = 2
        else:
            self.__priority = 1  
        self.__magnitude = magnitude
        self.__id = id

    def get_priority(self):
        """
        Gets the priority of the seismic event.

        Returns:
            int: The priority level (1, 2, or 3, where 3 is the highest).
        """
        return self.__priority

    def __eq__(self, other):
        """
        Checks if two Key instances are equal based on their ID.

        Args:
            other (Key): The other Key instance to compare with.

        Returns:
            bool: True if the IDs are equal, False otherwise.
        """
        return self.__id == other.__id

    def __lt__(self, other):
        """
        Determines if this Key is less than another Key.

        Comparison is done in the following order:
        1. Priority
        2. Magnitude
        3. ID

        Args:
            other (Key): The other Key instance to compare with.

        Returns:
            bool: True if this Key is strictly less than the other Key.
        """
        if self.__priority != other.__priority:
            return self.__priority < other.__priority

        if self.__magnitude != other.__magnitude:
            return self.__magnitude < other.__magnitude

        return self.__id < other.__id

    def __gt__(self, other):
        """
        Determines if this Key is greater than another Key.

        Comparison is done in the following order:
        1. Priority
        2. Magnitude
        3. ID

        Args:
            other (Key): The other Key instance to compare with.

        Returns:
            bool: True if this Key is strictly greater than the other Key.
        """
        if self.__priority != other.__priority:
            return self.__priority > other.__priority

        if self.__magnitude != other.__magnitude:
            return self.__magnitude > other.__magnitude

        return self.__id > other.__id

    def __repr__(self):
        """
        Returns a string representation of the Key.

        Returns:
            str: A string in the format "(priority, magnitude, id)".
        """
        return f"({self.__priority}, {self.__magnitude}, {self.__id})"
