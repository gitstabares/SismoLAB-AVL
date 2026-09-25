class Key:

    def __init__(self, magnitude, deepness, populated, event_id):

        if magnitude >= 6.0 or (magnitude >= 4.5 and deepness <= 30 and populated):
            self.__priority = 3
        elif magnitude >= 4.5:
            self.__priority = 2
        else:
            self.__priority = 1

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