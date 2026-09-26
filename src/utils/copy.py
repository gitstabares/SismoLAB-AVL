def copy(obj):
    """
    Creates a deep copy of an object, handling primitive types, iterables, and custom objects,
    while avoiding infinite recursion in case of circular references.

    Args:
        obj: The object to be copied.

    Returns:
        A new deep copy of the original object.
    """
    
    # memo contains the objects already copied, to avoid circular references
    memo = {}
    
    def __copy(__obj):
        """
        Recursive helper function to perform the actual deep copying.
        
        Args:
            __obj: The current object or sub-object being copied.
            
        Returns:
            A copy of __obj.
        """
        # It isn't needed to copy primitives
        primitive_types = (int, str, float, bool, type(None))
        # The iterables require recursive copy to their items
        if isinstance(__obj, primitive_types): 
            return __obj
        if isinstance(__obj, list): 
            return [__copy(i) for i in __obj]
        if isinstance(__obj, tuple): 
            return (__copy(i) for i in __obj)
        if isinstance(__obj, dict): 
            return {__copy(k): __copy(v) for k, v in __obj.items()}
            
        # Verifying if the object to copy has already been copied
        # This handles circular references
        if __obj in memo: 
            return memo[__obj]
            
        # Creating a new empty object without calling __init__
        new_obj = type(__obj).__new__(type(__obj))
        memo[__obj] = new_obj
        
        # Recursively copy all attributes of the object
        for k, v in __obj.__dict__.items():
            setattr(new_obj, k, __copy(v))
            
        return new_obj
        
    return __copy(obj)