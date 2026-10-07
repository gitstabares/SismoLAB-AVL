"""Serialize and deserialize Python objects as JSON-compatible data.

This module provides a serializer for primitive values, collections,
dates, custom classes, and cyclic object graphs.
"""

import json
from collections import deque
from datetime import datetime


class Serializer:
    """Serialize and deserialize complex Python objects as JSON-compatible data.

    The serializer supports primitive values, tuples, lists, deques, sets,
    dictionaries, datetime objects, and registered custom classes. Circular
    references are preserved through object identifiers stored in the serialized
    representation.
    """

    def __init__(self):
        """Initialize the serializer with an empty custom-class registry.

        Returns:
            None: Creates an empty class registry on the serializer instance.
        """
        self.classes = {}

    def register(self, classes):
        """Register a custom class for serialization and deserialization.

        Args:
            classes (type): The class to register.
        """
        name = classes.__module__ + "." + classes.__name__
        self.classes[name] = classes

    def serialize(self, obj):
        """Serialize an object into a JSON-compatible representation.

        Args:
            obj (Any): The object to serialize.

        Returns:
            Any: A JSON-compatible representation of ``obj``.

        Raises:
            TypeError: If ``obj`` is an instance of an unregistered custom class.
        """
        memo: set[int] = set()

        def convert(obj):
            """Convert an object into its serialized representation.

            Args:
                obj (Any): The object to convert.

            Returns:
                Any: The serialized representation of ``obj``.

            Raises:
                TypeError: If ``obj`` is an instance of an unregistered custom class.
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

            # Sets
            if isinstance(obj, set):
                return {
                    "$id": identity,
                    "$type": "set",
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

    def deserialize(self, data):
        """Deserialize a JSON-compatible value into its original Python object.

        Args:
            data (Any): The serialized data to rebuild.

        Returns:
            Any: The reconstructed Python object.

        Raises:
            ValueError: If ``data`` contains an unknown serialized type.
            KeyError: If a required serialized field is missing.
        """
        memo = {}

        def rebuild(element):
            """Rebuild a serialized object or value.

            Args:
                element (Any): The serialized element to rebuild.

            Returns:
                Any: The reconstructed Python object or value.

            Raises:
                ValueError: If ``element`` contains an unknown serialized type.
                KeyError: If a required serialized field is missing.
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

            # Sets
            if obj_type == "set":
                obj_set = set([rebuild(item) for item in element["items"]])
                memo[element["$id"]] = obj_set
                return obj_set
            
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
    
    def save(self, scenario, path):
        """Serialize an object and write it to a JSON file.

        Args:
            scenario (Any): The object to serialize and save.
            path (str): The destination file path.
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

    def load(self, path):
        """Load and deserialize an object from a JSON file.

        Args:
            path (str): The source file path.

        Returns:
            Any: The deserialized Python object.

        Raises:
            ValueError: If the JSON contains an unknown serialized type.
            FileNotFoundError: If ``path`` does not exist.
            json.JSONDecodeError: If the file does not contain valid JSON.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.deserialize(data)