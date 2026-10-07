"""Utilities for storing and checking populated zones.

This module defines a set of circular populated zones. A point is considered to
belong to a populated zone when its distance from the zone's center is less than
or equal to the zone's radius.
"""

from .point import Point


class PopulatedZones(set):
    """A set of circular populated zones.

    The set behaves like a normal Python set, while its membership checks use
    each zone's center and radius to determine whether a point falls inside one of
    the zones.
    """

    def __contains__(self, point: Point) -> bool:
        """Check if an point is in the set.

        Args:
            point (Any): The point to check.

        Returns:
            bool: True if the point is in the populated zones, False otherwise.
        """
        for circle in self:
            if (circle.get_center() - point).get_lenght() <= circle.get_radius():
                return True
        return False