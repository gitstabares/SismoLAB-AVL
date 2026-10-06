from collections import deque
import datetime as dt


def copy(obj):
    """
    Creates a deep copy of an object, handling primitive types, iterables, and custom objects.

    This function avoids infinite recursion in case of circular references.

    Args:
        obj (T): The object to be copied.

    Returns:
        T: A new deep copy of the original object.
    """
    # memo contains the objects already copied, to avoid circular references
    memo = {}
    
    def __copy(_obj):
        """
        Recursive helper function to perform the actual deep copying.
        
        Args:
            __obj (Any): The current object or sub-object being copied.
            
        Returns:
            Any: A deep copy of __obj.
        """
        # It isn't needed to copy primitives
        primitive_types = (int, str, float, bool, type(None))
        
        if isinstance(_obj, primitive_types): 
            return _obj
        if isinstance(_obj, list): 
            return [__copy(i) for i in _obj]
        if isinstance(_obj, tuple): 
            return (__copy(i) for i in _obj)
        if isinstance(_obj, dict): 
            return {__copy(k): __copy(v) for k, v in _obj.items()}
        if isinstance(_obj, deque):
            return deque([__copy(i) for i in _obj])
        if isinstance(_obj, set):
            return set([__copy(i) for i in _obj])
        if isinstance(_obj, dt.datetime):
            return _obj.replace()
            
        # Verifying if the object to copy has already been copied
        obj_id = id(_obj)
        if obj_id in memo: 
            return memo[obj_id]
            
        # Creating a new empty object without calling __init__
        new_obj = type(_obj).__new__(type(_obj))
        memo[obj_id] = new_obj
        
        # Recursively copy all attributes of the object
        for k, v in _obj.__dict__.items():
            setattr(new_obj, k, __copy(v))
            
        return new_obj
        
    return __copy(obj)