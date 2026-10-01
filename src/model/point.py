from typing import Any

class Point(tuple):
    """A two-dimensional point with coordinates clamped to the 0-1000 range."""

    def __new__(cls, x: float, y: float) -> 'Point':
        """Create a Point object, validating bounds.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.

        Returns:
            Point: A new Point instance.

        Raises:
            ValueError: If either coordinate is outside the [0, 1000] range.
        """
        if not (0 <= x <= 1000) or not (0 <= y <= 1000):
            raise ValueError(f"both coordinates must be between 0 and 1000. Got: ({x},{y})")
        return super().__new__(cls, [round(x, 1), round(y, 1)])

    @property
    def x(self) -> float:
        """float: The x-coordinate of the point."""
        return self[0]

    @property
    def y(self) -> float:
        """float: The y-coordinate of the point."""
        return self[1]
    
    def __add__(self, other: Any) -> 'Point':
        """Return the coordinate-wise sum as a new point.

        Args:
            other (Any): The point to add.

        Returns:
            Point: A new point representing the sum.

        Raises:
            TypeError: If the other operand is not a Point.
        """
        if not isinstance(other, Point): 
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Any) -> 'Point':
        """Return the coordinate-wise difference as a new point.

        Args:
            other (Any): The point to subtract.

        Returns:
            Point: A new point representing the difference.

        Raises:
            TypeError: If the other operand is not a Point.
        """
        if not isinstance(other, Point): 
            raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")
        return Point(self.x - other.x, self.y - other.y)

    def __mod__(self, divisor: float) -> 'Point':
        """Return the coordinate-wise modulus using the given divisor.

        Args:
            divisor (float): The divisor for the modulo operation.

        Returns:
            Point: A new point resulting from the modulo operation.
        """
        return Point(self.x % divisor, self.y % divisor)
        
    def get_length(self) -> float:
        """Return the Euclidean distance from the origin.

        Returns:
            float: The distance from the origin (0, 0).
        """
        return (self.x**2 + self.y**2)**(1/2)