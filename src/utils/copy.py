from typing import Any, Dict, TypeVar

T = TypeVar('T')

def copy(obj: T) -> T:
    """
    Creates a deep copy of an object, handling primitive types, iterables, and custom objects.

    This function avoids infinite recursion in case of circular references.

    Args:
        obj (T): The object to be copied.

    Returns:
        T: A new deep copy of the original object.
    """
    # memo contains the objects already copied, to avoid circular references
    memo: Dict[int, Any] = {}
    
    def __copy(__obj: Any) -> Any:
        """
        Recursive helper function to perform the actual deep copying.
        
        Args:
            __obj (Any): The current object or sub-object being copied.
            
        Returns:
            Any: A deep copy of __obj.
        """
        # It isn't needed to copy primitives
        primitive_types = (int, str, float, bool, type(None))
        
        if isinstance(__obj, primitive_types): 
            return __obj
        if isinstance(__obj, list): 
            return [__copy(i) for i in __obj]
        if isinstance(__obj, tuple): 
            return (__copy(i) for i in __obj)
        if isinstance(__obj, dict): 
            return {__copy(k): __copy(v) for k, v in __obj.items()}
            
        # Verifying if the object to copy has already been copied
        obj_id = id(__obj)
        if obj_id in memo: 
            return memo[obj_id]
            
        # Creating a new empty object without calling __init__
        new_obj = type(__obj).__new__(type(__obj))
        memo[obj_id] = new_obj
        
        # Recursively copy all attributes of the object
        for k, v in __obj.__dict__.items():
            setattr(new_obj, k, __copy(v))
            
        return new_obj
        
    return __copy(obj)