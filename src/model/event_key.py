class EventKey:
    def __init__(self,priority,magnitude,event_id):
        self.__priority = priority
        self.__magnitude = magnitude
        self.__event_id = event_id 
   
    def get_priority(self):
        return self.__priority

    def get_magnitude(self):
        return self.__magnitude

    def get_event_id(self):
        return self.__event_id

    def __lt__(self, other):
        if self.__priority != other.__priority:
            return self.__priority < other.__priority

        if self.__magnitude != other.__magnitude:
            return self.__magnitude < other.__magnitude

        return self.__event_id < other.__event_id

    def __eq__(self, other):
        return (
            self.__priority == other.__priority
            and self.__magnitude == other.__magnitude
            and self.__event_id == other.__event_id
        )

    def __repr__(self):
        return f"({self.__priority}, {self.__magnitude}, {self.__event_id})"