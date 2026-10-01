import json
from collections import deque
from datetime import datetime
from typing import Any, Dict, Type


class Serializer:
    """
    A class to serialize and deserialize complex Python objects, including custom classes,
    lists, dictionaries, deques, and datetime objects, into/from JSON-compatible formats.
    
    It handles circular references by using a memoization strategy.
    """

    def __init__(self) -> None:
        """
        Initializes the Serializer with an empty registry for custom classes.
        """
        self.classes: Dict[str, Type] = {}

    def register(self, classes: Type) -> None:
        """
        Registers a custom class so that the serializer knows how to serialize
        and deserialize its instances.

        Args:
            classes (Type): The class type to register.
        """
        name = classes.__module__ + "." + classes.__name__
        self.classes[name] = classes

    def serialize(self, obj: Any) -> Any:
        """
        Serializes an object into a JSON-compatible dictionary format.

        Args:
            obj (Any): The object to serialize.

        Returns:
            Any: The serialized representation of the object (dict or primitive).
        """
        memo: set[int] = set()

        def convert(obj: Any) -> Any:
            """
            Recursive helper function to convert an object into its serialized form.

            Args:
                obj (Any): The object to convert.

            Returns:
                Any: The converted representation of the object.
            """
            # Primitive types
            if obj is None or type(obj) in (int, str, float, bool):
                return obj

            # Dates
            if isinstance(obj, datetime):
                return {
                    "$type": "datetime",
                    "value": obj.isoformat()
                }

            # Check previous references to avoid infinite recursion (circular references)
            identity = id(obj)

            if identity in memo:
                return {"$ref": identity}

            # Assign internal id for the object
            memo.add(identity)

            # Tuples
            if isinstance(obj, tuple):
                return {
                    "$id": identity,
                    "$type": "tuple",
                    "items": [convert(x) for x in obj]
                }
            
            # Lists
            if isinstance(obj, list):
                return {
                    "$id": identity,
                    "$type": "list",
                    "items": [convert(x) for x in obj]
                }

            # Queues
            if isinstance(obj, deque):
                return {
                    "$id": identity,
                    "$type": "deque",
                    "items": [convert(x) for x in obj]
                }

            # Dictionaries
            if isinstance(obj, dict):
                return {
                    "$id": identity,
                    "$type": "dict",
                    "items": [[convert(k), convert(v)] for k, v in obj.items()]
                }

            # Personalized (custom) objects
            classes = type(obj)
            name = classes.__module__ + "." + classes.__name__

            if self.classes.get(name) is not classes:
                raise TypeError(f"not registered class: {name}")

            return {
                "$id": identity,
                "$type": "object",
                "class": name,
                "attributes": {k: convert(v) for k, v in vars(obj).items()}
            }

        return convert(obj)

    def deserialize(self, data: Any) -> Any:
        """
        Deserializes a JSON-compatible dictionary format back into a Python object.

        Args:
            data (Any): The serialized data to reconstruct.

        Returns:
            Any: The reconstructed Python object.
        
        Raises:
            ValueError: If an unknown type is encountered.
        """
        memo: Dict[int, Any] = {}

        def rebuild(element: Any) -> Any:
            """
            Recursive helper function to rebuild an object from its serialized form.

            Args:
                element (Any): The serialized element to rebuild.

            Returns:
                Any: The rebuilt Python object or value.
            """
            # Primitive types
            if not isinstance(element, dict):
                return element

            # Reference to an existing object (handling circular references)
            if "$ref" in element:
                return memo[element["$ref"]]

            obj_type = element.get("$type")

            # Dates
            if obj_type == "datetime":
                return datetime.fromisoformat(element["value"])

            if obj_type == "tuple":
                obj_tuple = tuple(rebuild(item) for item in element["items"])
                memo[element["$id"]] = obj_tuple
                return obj_tuple

            # Lists
            if obj_type == "list":
                obj_list = [rebuild(item) for item in element["items"]]
                memo[element["$id"]] = obj_list
                return obj_list

            # Queues
            if obj_type == "deque":
                obj_deque = deque([rebuild(item) for item in element["items"]])
                memo[element["$id"]] = obj_deque
                return obj_deque
            
            # Dictionaries
            if obj_type == "dict":
                obj_dict = {rebuild(key): rebuild(value) for key, value in element["items"]}
                memo[element["$id"]] = obj_dict
                return obj_dict

            # Personalized (custom) objects
            if obj_type == "object":
                classes = self.classes[element["class"]]

                # Create the empty instance without calling __init__
                obj_custom = object.__new__(classes)

                # Register it before building its attributes to handle circular dependencies
                memo[element["$id"]] = obj_custom

                for name, value in element["attributes"].items():
                    setattr(obj_custom, name, rebuild(value))

                return obj_custom

            raise ValueError(f"Unknown type: {obj_type}")

        return rebuild(data)
    
    def save(self, scenario: Any, path: str) -> None:
        """
        Serializes an object and saves it to a JSON file.

        Args:
            scenario (Any): The object to serialize and save.
            path (str): The file path where the JSON data will be written.
        """
        data = self.serialize(scenario)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
                allow_nan=False
            )

    def load(self, path: str) -> Any:
        """
        Loads JSON data from a file and deserializes it back into a Python object.

        Args:
            path (str): The file path to load the JSON data from.

        Returns:
            Any: The deserialized Python object.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.deserialize(data)