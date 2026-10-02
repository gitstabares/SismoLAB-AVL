from src.core import Point


class PopulatedZones(set):
    """A collection of rounded populated zones."""

    def __contains__(self, point: Point):
        """Check if an point is in the set.

        Args:
            point (Any): The point to check.

        Returns:
            bool: True if the point is in the populated zones, False otherwise.
        """
        for circle in self:
            if (circle.center - point).length <= circle.radius:
                return True
        return False