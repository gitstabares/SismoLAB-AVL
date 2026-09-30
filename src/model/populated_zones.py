from .point import Point


class PopulatedZones(set):

    def __init__(self, distance):
        self.__distance = distance

    def get_distance(self):
        return self.__distance

    def set_distance(self, distance):
        self.__distance = distance

    def add(self, element):
        if not isinstance(element, Point): raise TypeError("must be Point")
        point = element - element % self.__distance
        super().add(point)

    def add_many(self, iterable):
        if isinstance(iterable,Point):
            super().add(iterable)
            return
        for element in iterable:
            self.add(element)

    def __contains__(self, element):
        point = element - element % self.__distance
        return super().__contains__(point)