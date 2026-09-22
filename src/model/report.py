from .tree import tree
class Report:
    def __init__(self, magnitude, depth, epicenter, date, origin_station, review, id):
        self.id = id
        self.magnitude = magnitude
        self.depth = depth
        self.epicenter = epicenter
        self.date = date
        self.origin_station = origin_station
        self.review = review
        
    def get_magnitude(self):
        return self.magnitude
    
    def get_depth(self):
        return self.depth
    
    def get_epicenter(self):
        return self.epicenter
    
    def get_date(self):
        return self.date
    
    def get_origin_station(self):
        return self.origin_station
    
    def get_review(self):
        return self.review
    
    def get_id(self):
        return self.id