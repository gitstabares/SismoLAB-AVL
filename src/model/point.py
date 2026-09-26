class Point:
    def __init__(self, x, y):
        self.x = max(0, min(1000, x))
        self.y = max(0, min(1000, y))
        
    def __add__(self,other):
        return Point(self.x + other.x,self.y + other.y)
    
    def __sub__(self,other):
        return Point(self.x - other.x,self.y - other.y)
        
    def get_length(self):
        return (self.x**2 + self.y**2)**(1/2)