from src.model import Key
from src.model import Node

class Event(Node):

    def __init__(
        self,
        id,
        magnitude,
        deepness,
        epicenter,
        date,
        review,
        origin_station,
        revised,
        is_populated
    ):
        super().__init__(Key(magnitude, deepness, is_populated, id))
        self.__id = id
        self.__magnitude = magnitude
        self.__deepness = deepness
        self.__epicenter = epicenter
        self.__date = date
        self.__review = review
        self.__origin_station = origin_station
        self.__revised = revised
        self.__is_populated = is_populated
        self.__aftershocks = []
        self.__costly_access = False

    def get_id(self):
        return self.__id

    def get_magnitude(self):
        return self.__magnitude

    def set_magnitude(self, magnitude):
        self.__magnitude = magnitude

    def get_deepness(self):
        return self.__deepness

    def set_deepness(self, deepness):
        self.__deepness = deepness

    def get_epicenter(self):
        return self.__epicenter

    def set_epicenter(self, epicenter):
        self.__epicenter = epicenter

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_review(self):
        return self.__review

    def set_review(self, review):
        self.__review = int(review)

    def get_origin_station(self):
        return self.__origin_station

    def set_origin_station(self, origin_station):
        self.__origin_station = origin_station

    def get_revised(self):
        return self.__revised

    def set_revised(self, revised):
        self.__revised = revised

    def get_costly_access(self):
        return self.__costly_access

    def get_aftershocks(self):
        return self.__aftershocks

    def update_aftershocks(self, W = 48, R = 40):
        def add_aftershock(root):
            if not root:
                return
            if root.get_magnitude() < self.__magnitude and 0 < (root.get_date() - self.__date).days < W/24 and (root.get_epicenter() - self.__epicenter).get_length() < R:
                self.__aftershocks.append(root)
            root.get_left().update_aftershocks()
            root.get_right().update_aftershocks()
        add_aftershock(self.get_root())

    def update_costly_access(self, L = 3):
        self.__costly_access = self.__key.get_priority() == 3 and self.get_depth() > L

    def update_key(self):
        self.__key = Key(self.__magnitude, self.__deepness, self.__is_populated, self.__id)