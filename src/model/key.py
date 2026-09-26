class Key:

    def __init__(self, magnitude, deepness, is_populated, id):
        if magnitude >= 4.5:
            if magnitude >= 6.0 or (deepness <= 30 and is_populated):
                self.__priority = 3
            else:
                self.__priority = 2
        else:
            self.__priority = 1  
        self.__magnitude = magnitude
        self.__id = id

    def get_priority(self):
        return self.__priority

    def __eq__(self, other):
        return self.__id == other.__id

    def __lt__(self, other):
        if self.__priority != other.__priority:
            return self.__priority < other.__priority

        if self.__magnitude != other.__magnitude:
            return self.__magnitude < other.__magnitude

        return self.__id < other.__id

    def __gt__(self, other):
        if self.__priority != other.__priority:
            return self.__priority > other.__priority

        if self.__magnitude != other.__magnitude:
            return self.__magnitude > other.__magnitude

        return self.__id > other.__id

    def __repr__(self):
        return f"({self.__priority}, {self.__magnitude}, {self.__id})"
