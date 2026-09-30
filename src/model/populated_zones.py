class PopulatedZones(set):

    def __init__(self, distance):
        self.__distance = distance

    def get_distance(self):
        return self.__distance

    def set_distance(self, distance):
        self.__distance = distance
        new_values = {
            element - element % self.__distance
            for element in self
        }

        self.clear()
        self.update(new_values)

    def add(self, element):
        point = element - element % self.__distance
        super().add(point)

    def __contains__(self, element):
        point = element - element % self.__distance
        return super().__contains__(point)