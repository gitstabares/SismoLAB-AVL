"""Provide a recursive copy helper for common Python objects.

The :func:`copy` function handles primitive values, selected built-in
containers, datetimes, and custom objects with instance attributes.
"""

from collections import deque
import datetime as dt


def copy(obj):
    """Recursively copy an object using the supported type-specific rules.

    Primitive values are returned unchanged. Lists, dictionaries, deques, and
    sets are rebuilt recursively; datetimes are copied with ``replace()``.
    Tuple inputs currently produce a generator of copied elements. Other
    objects are allocated without calling ``__init__`` and their attributes
    are copied recursively. A memo is used for custom objects to preserve
    repeated references and handle cycles among those objects.

    Args:
        obj: The object to copy.

    Returns:
        The copied object, or the original value for primitive types.

    Note:
        The memo is applied only to custom objects. Cycles involving built-in
        containers are therefore not guaranteed to be handled.
    """
    # memo contains the objects already copied, to avoid circular references
    memo = {}
    
    def __copy(_obj):
        """Recursively copy a value according to its type.

        Args:
            _obj: The current object or nested value to copy.

        Returns:
            The copied value.
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