class Point(tuple):
    """A two-dimensional point with coordinates clamped to the 0–1000 range."""

    def __new__(cls, x, y):
        """Create a Point object, validating bounds."""
        if not (0 <= x <= 1000) or not (0 <= y <= 1000):
            raise ValueError(f"both coordinates must be between 0 and 1000. Got: ({x},{y})")
        return super().__new__(cls, [round(x,1),round(y,1)])

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