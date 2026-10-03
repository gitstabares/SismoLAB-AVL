from .point import Point


class Circle(tuple):
    def __new__(cls, center:Point, radius:float):
        return super().__new__(cls,[center,radius])

    @property
    def center(self) -> Point:
        return self[0]

    @property
    def radius(self) -> float:
        return self[1]

    def __repr__(self):
        return f"(C={self.center},R={self.radius})"