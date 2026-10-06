from .point import Point


class Circle():
    def __init__(self, center:Point, radius:float):
        self._center = center
        self._radius = radius

    def __repr__(self):
        return f"(C={self.get_center()},R={self.get_radius()})"

    def get_center(self) -> Point:
        return self._center

    def get_radius(self) -> float:
        return self._radius