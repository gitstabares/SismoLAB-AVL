from .point import Point


class Circle(tuple):
    def __new__(cls, center:Point, radius:float):
        return super().__new__(cls,[center,radius])

    def __repr__(self):
        return f"(C={self.get_center()},R={self.get_radius()})"

    def get_center(self) -> Point:
        return self[0]

    def get_radius(self) -> float:
        return self[1]