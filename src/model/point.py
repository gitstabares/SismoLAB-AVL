class Point():
    """Represent a two-dimensional point.

    The point can store any numeric coordinates; bounds are not currently
    enforced during initialization.
    """

    def __init__(self, x: float, y: float):
        """Initialize a point with the given coordinates.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.

        Raises:
            Exception: If either coordinate is None.
        """
        if x is None or y is None:
            raise Exception("No coordinate can be none")
        self._x = x
        self._y = y

    def get_x(self) -> float:
        """Return the x-coordinate.

        Returns:
            float: The x-coordinate of the point.
        """
        return self._x

    def get_y(self) -> float:
        """Return the y-coordinate.

        Returns:
            float: The y-coordinate of the point.
        """
        return self._y

    def get_length(self) -> float:
        """Return the Euclidean distance from the origin.

        Returns:
            float: The distance from the origin (0, 0).
        """
        return (self.get_x()**2 + self.get_y()**2)**(1/2)

    def __eq__(self, other: Point) -> bool:
        """Return whether the point is equal to another point or coordinate pair.

        Args:
            other (Point | tuple | list): The point or coordinate pair to compare
                against.

        Returns:
            bool: True if both coordinates are equal; otherwise, False.
        """
        if isinstance(other, (tuple, list)):
            return self.get_x() == other[0] and self.get_y() == other[1]
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __add__(self, other: Point):
        """Return a new point containing the coordinate-wise sum.

        Args:
            other (Point): The point to add.

        Returns:
            Point: A new point representing the sum.
        """
        return Point(self.get_x() + other.get_x(), self.get_y() + other.get_y())

    def __sub__(self, other: Point):
        """Return a new point containing the coordinate-wise difference.

        Args:
            other (Point): The point to subtract.

        Returns:
            Point: A new point representing the difference.
        """
        return Point(self.get_x() - other.get_x(), self.get_y() - other.get_y())

    def __mod__(self, divisor: float):
        """Return a new point containing the coordinate-wise modulo.

        Args:
            divisor (float): The value used as the modulo divisor.

        Returns:
            Point: A new point resulting from the modulo operation.
        """
        return Point(self.get_x() % divisor, self.get_y() % divisor)

    def __repr__(self):
        """Return the point as a readable coordinate representation.

        Returns:
            str: The point coordinates in the form "(x,y)".
        """
        return f"({self._x},{self._y})"