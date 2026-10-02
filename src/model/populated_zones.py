class PopulatedZones(set):
    """A collection of populated zones, aligned to a grid tile size.
    
    Attributes:
        __tile_size (float): The size of the grid tiles.
    """

    def __init__(self, tile_size):
        """Initialize the PopulatedZones with a given tile size.

        Args:
            tile_size (float): The grid tile size used to align elements.
        """
        self.__tile_size = tile_size
        super().__init__()

    def get_distance(self):
        """Get the current tile size distance.

        Returns:
            float: The tile size distance.
        """
        return self.__tile_size

    def set_distance(self, tile_size):
        """Set a new tile size distance and realign all elements.

        Args:
            tile_size (float): The new tile size.
        """
        self.__tile_size = tile_size
        new_values = {
            element - element % self.__tile_size
            for element in self
        }

        self.clear()
        self.update(new_values)

    def add(self, element):
        """Add an element, aligning it to the grid based on the tile size.

        Args:
            element (Point): The element to add.
        """
        point = element - element % self.__tile_size
        super().add(point)

    def __contains__(self, element):
        """Check if an element is in the set, matching grid alignment.

        Args:
            element (Any): The element to check.

        Returns:
            bool: True if the element is in the populated zones, False otherwise.
        """
        point = element - element % self.__tile_size
        return super().__contains__(point)