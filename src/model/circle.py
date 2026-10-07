"""Circle model representing a geometric circle."""

from .point import Point


class Circle:
    """Represents a circle defined by its center and radius.

    Attributes:
        _center (Point): Center point of the circle.
        _radius (float): Radius of the circle.
    """

    def __init__(self, center: Point, radius: float):
        """Initialize a circle.

        Args:
            center (Point): Center point of the circle.
            radius (float): Radius of the circle.
        """
        self._center = center
        self._radius = radius

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the circle.

        Returns:
            str: The center and radius in the format ``(C=...,R=...)``.
        """
        return f"(C={self.get_center()},R={self.get_radius()})"

    def get_center(self) -> Point:
        """Return the center point of the circle.

        Returns:
            Point: Center point of the circle.
        """
        return self._center

    def get_radius(self) -> float:
        """Return the radius of the circle.

        Returns:
            float: Radius of the circle.
        """
        return self._radius