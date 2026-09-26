from model.tree import Tree

class EventTree(Tree):
    def __init__(self, root=None):
        super().__init__(root)

    def update_aftershocks(self, W = 48, R = 40):
        for seism in self.get_levelorder_traverse():
            for aftershock in self.get_levelorder_traverse():
                if seism.get_magnitude() > aftershock.get_magnitude() and 0 < (aftershock.get_date() - seism.get_date()).days < W/24 and (aftershock.get_epicenter() - seism.get_epicenter()).get_length() < R:
                    seism.get_aftershocks().append(aftershock)

    def update_costly_access(self, L = 3):
        for seism in self.get_levelorder_traverse():
            seism.set_costly_access(seism.get_key().get_priority() == 3 and seism.get_depth() > L)