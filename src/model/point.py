class Point(tuple):
    """A two-dimensional point with coordinates clamped to the 0-1000 range."""

    def __new__(cls, x:float, y:float):
        """Create a Point object, validating bounds.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.

        Returns:
            Point: A new Point instance.

        Raises:
            ValueError: If either coordinate is outside the [0, 1000] range.
        """
        return super().__new__(cls, [round(x, 1), round(y, 1)])

    def get_x(self) -> float:
        """float: The x-coordinate of the point."""
        return self[0]

    def get_y(self) -> float:
        """float: The y-coordinate of the point."""
        return self[1]

    def get_length(self) -> float:
        """Return the Euclidean distance from the origin.

        Returns:
            float: The distance from the origin (0, 0).
        """
        return (self.get_x()**2 + self.get_y()**2)**(1/2)
    
    def __add__(self, other:Point):
        """Return the coordinate-wise sum as a new point.

        Args:
            other (Any): The point to add.

        Returns:
            Point: A new point representing the sum.

        Raises:
            TypeError: If the other operand is not a Point.
        """
        return Point(self.get_x() + other.get_x(), self.get_y() + other.get_y())
    
    def __sub__(self, other:Point):
        """Return the coordinate-wise difference as a new point.

        Args:
            other (Any): The point to subtract.

        Returns:
            Point: A new point representing the difference.

        Raises:
            TypeError: If the other operand is not a Point.
        """
        return Point(self.get_x() - other.get_x(), self.get_y() - other.get_y())

    def __mod__(self, divisor:float):
        """Return the coordinate-wise modulus using the given divisor.

        Args:
            divisor (float): The divisor for the modulo operation.

        Returns:
            Point: A new point resulting from the modulo operation.
        """
        return Point(self.get_x() % divisor, self.get_y() % divisor)