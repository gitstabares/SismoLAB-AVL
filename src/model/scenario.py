from .populated_zones import PopulatedZones
from .event_tree import EventTree
from .event import Event


class Scenario:
    def __init__(self, tile_size):
        self.__AVL = EventTree(autobalance=True)
        self.__BST = EventTree()
        self.__populated_zones = PopulatedZones(tile_size)
        self.__archived_AVL_trees = set()
        self.__archived_BST_trees = set()
        self.__eliminated_nodes = set()

    def archive_event(self,key):
        self.__archived_AVL_trees.add(self.__AVL.archive(key))
        self.__archived_BST_trees.add(self.__BST.archive(key))

    def insert_report(self,report):
        if report.get_id() in self.__eliminated_nodes:
            raise Exception("The ID registered was used previously and currently is deleted.")
        new_event = Event(report,
                          report.get_epicenter() in self.__populated_zones)
        if new_event.get_key() not in self.__AVL:
            self.__AVL.add_node(new_event)
            self.__BST.add_node(new_event)
        else:
            actual_AVL = self.__AVL.get_node(report.get_id())
            actual_BST = self.__BST.get_node(report.get_id())
            if new_event.get_review() > actual_AVL.get_review():
                if new_event.get_key().get_tuple() != actual_AVL.get_key().get_tuple():
                    self.__AVL.pop_node(actual_AVL.get_key())
                    self.__BST.pop_node(actual_BST.get_key())
                    self.__AVL.add_node(new_event)
                    self.__BST.add_node(new_event)
                else:
                    actual_AVL.set_all(new_event)
                    actual_BST.set_all(new_event)
                self.__AVL.update_aftershocks()
                self.__AVL.update_costly_access()
                self.__BST.update_aftershocks()
                self.__BST.update_costly_access()
            elif new_event.get_review() == actual_AVL.get_review():
                if new_event.get_all() == actual_AVL.get_all():
                    actual_AVL.set_revised(True)
                    actual_BST.set_revised(True)
                    if not actual_AVL.get_origin_station():
                        actual_AVL.set_origin_station(new_event.get_origin_station())
                        actual_BST.set_origin_station(new_event.get_origin_station())
                else:
                    raise Exception("There's an event in the tree with different data and same review.")
            else:
                raise Exception("Report's information too old. There's newer information in the tree.")

    def delete_event(self, identifier):
        self.__AVL.pop_node(identifier)
        self.__BST.pop_node(identifier)
        self.__eliminated_nodes.add(identifier)

    def get_event_AVL(self,identifier):
        return self.__AVL.get_node(identifier)

    def get_event_BST(self,identifier):
        return self.__BST.get_node(identifier)

    def set_stress_mode(self,value):
        self.__AVL.set_autobalance(value)

    def set_W(self, W):
        self.__AVL.set_W(W)
        self.__BST.set_W(W)

    def set_R(self, R):
        self.__AVL.set_R(R)
        self.__BST.set_R(R)

    def set_L(self, L):
        self.__AVL.set_L(L)
        self.__BST.set_L(L)