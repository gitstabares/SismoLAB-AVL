from .populated_zones import PopulatedZones
from .event_tree import EventTree
from .event import Event


class Scenario:
    def __init__(self, tile_size):
        self.__AVL = EventTree(autobalance=True)
        self.__BST = EventTree()
        self.__populated_zones = PopulatedZones(tile_size)

    def insert_report(self,report):
        new_event = Event(report,
                          report.get_epicenter() in self.__populated_zones)
        if new_event.get_key() not in self.__AVL:
            self.__AVL.add_node(new_event)
            self.__BST.add_node(new_event)
        else:
            actual_event = self.__AVL.get_node(report.get_id())
            if new_event.get_review() > actual_event.get_review():
                #UPDATE DATA IN BOTH TREES
                pass
            elif 

    def delete_event(self, identifier):
        self.__AVL.pop_node(identifier)
        self.__BST.pop_node(identifier)

    def get_event(self,identifier):
        self.__AVL.get_node(identifier)

    def set_stress_mode(self,value):
        self.__AVL.set_autobalance(value)