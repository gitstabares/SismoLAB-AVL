from datetime import datetime


class Event:

    def __init__(
        self,
        event_id,
        magnitude,
        depth,
        x,
        y,
        timestamp,
        revision,
        stations,
        attention
    ):
        self.__event_id = event_id
        self.__magnitude = magnitude
        self.__depth = depth
        self.__x = x
        self.__y = y
        self.__timestamp = timestamp
        self.__revision = revision
        self.__stations = stations
        self.__attention = attention

    def get_event_id(self):
        return self.__event_id

    def get_magnitude(self):
        return self.__magnitude

    def get_depth(self):
        return self.__depth

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_timestamp(self):
        return self.__timestamp

    def get_revision(self):
        return self.__revision

    def get_stations(self):
        return self.__stations

    def get_attention(self):
        return self.__attention