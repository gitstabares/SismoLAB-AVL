class Point(tuple):
    """A two-dimensional point with coordinates clamped to the 0–1000 range."""

    def __new__(cls, x, y):
        """Initialize the point, clamping both coordinates to the valid range."""
        return super().__new__(cls, [max(0, min(1000, x)),max(0, min(1000, y))])

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
    
    def __add__(self,other):
        if not isinstance(other,Point): raise TypeError(f"unsupported operand type(s) for -: '{type(other).__name__}' and '{type(other).__name__}'")
        """Return the coordinate-wise sum as a new point."""
        return Point(self.x + other.x,self.y + other.y)
    
    def __sub__(self,other):
        if not isinstance(other,Point): raise TypeError(f"unsupported operand type(s) for -: '{type(other).__name__}' and '{type(other).__name__}'")
        """Return the coordinate-wise difference as a new point."""
        return Point(self.x - other.x,self.y - other.y)

    def __mod__(self,divisor):
        """Return the coordinate-wise modulus using the given divisor."""
        return Point(self.x % divisor, self.y % divisor)
        
    def get_length(self):
        """Return the Euclidean distance from the origin."""
        return (self.x**2 + self.y**2)**(1/2)