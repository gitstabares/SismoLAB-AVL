from src.model.node import Node


class Event(Node):

    def __init__(
        self,
        key,
        event_id,
        magnitude,
        deepness,
        epicenter,
        date,
        review,
        origin_station,
        revised,
        costly_access,
        aftershocks
    ):
        super().__init__(key)

        self.__id = event_id
        self.__magnitude = magnitude
        self.__deepness = deepness
        self.__epicenter = epicenter
        self.__date = date
        self.__review = review
        self.__origin_station = origin_station
        self.__revised = revised
        self.__costly_access = costly_access
        self.__aftershocks = aftershocks

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
        self.__review = review

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

    def set_costly_access(self, costly_access):
        self.__costly_access = costly_access

    def get_aftershocks(self):
        return self.__aftershocks

    def set_aftershocks(self, aftershocks):
        self.__aftershocks = aftershocks