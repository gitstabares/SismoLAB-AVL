import math
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self,other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        
        return Point(new_x,new_y)
    
    def __sub__(self,other):
        new_x = self.x - other.x
        new_y = self.y - other.y
            
        return Point(new_x,new_y)
        
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)