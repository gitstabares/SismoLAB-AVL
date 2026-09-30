class PopulatedZones(set):

    def __init__(self, tile_size):
        self.__tile_size = tile_size

    def get_distance(self):
        return self.__tile_size

    def set_distance(self, tile_size):
        self.__tile_size = tile_size
        new_values = {
            element - element % self.__tile_size
            for element in self
        }

        self.clear()
        self.update(new_values)

    def add(self, element):
        point = element - element % self.__tile_size
        super().add(point)

    def __contains__(self, element):
        point = element - element % self.__tile_size
        return super().__contains__(point)