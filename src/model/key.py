class Key:

    def __init__(self, priority, magnitude, event_id):
        self.__priority = priority
        self.__magnitude = magnitude
        self.__id = event_id

    def __eq__(self, other):
        return (
            self.__priority == other.__priority
            and self.__magnitude == other.__magnitude
            and self.__id == other.__id
        )

    def __lt__(self, other):
        if self.__priority != other.__priority:
            return self.__priority < other.__priority

        if self.__magnitude != other.__magnitude:
            return self.__magnitude < other.__magnitude

        return self.__id < other.__id

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __repr__(self):
        return f"({self.__priority}, {self.__magnitude}, {self.__id})"