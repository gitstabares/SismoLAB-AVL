class Point(list):
    """A two-dimensional point with coordinates clamped to the 0–1000 range."""

    def __init__(self, x, y):
        """Initialize the point, clamping both coordinates to the valid range."""
        self.x = max(0, min(1000, x))
        self.y = max(0, min(1000, y))
        super().__init__([self.x,self.y])
        
    def __add__(self,other):
        """Return the coordinate-wise sum as a new point."""
        return Point(self.x + other.x,self.y + other.y)
    
    def __sub__(self,other):
        """Return the coordinate-wise difference as a new point."""
        return Point(self.x - other.x,self.y - other.y)

    def __repr__(self):
        return f"({self.x},{self.y})"
        
    def get_length(self):
        """Return the Euclidean distance from the origin."""
        return (self.x**2 + self.y**2)**(1/2)