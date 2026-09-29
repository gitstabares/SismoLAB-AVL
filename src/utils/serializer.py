import json
from collections import deque
from datetime import datetime


class Serializer:
    """
    A class to serialize and deserialize complex Python objects, including custom classes,
    lists, dictionaries, deques, and datetime objects, into/from JSON-compatible formats.
    It handles circular references by using a memoization strategy.
    """

    def __init__(self):
        """
        Initializes the Serializer with an empty registry for custom classes.
        """
        self.classes = {}

    def register(self, classes):
        """
        Registers a custom class so that the serializer knows how to serialize
        and deserialize its instances.

        Args:
            classes (type): The class type to register.
        """
        name = classes.__module__ + "." + classes.__qualname__
        self.classes[name] = classes

    def serialize(self, obj):
        """
        Serializes an object into a JSON-compatible dictionary format.

        Args:
            obj: The object to serialize.

        Returns:
            dict or primitive: The serialized representation of the object.
        """
        memo = {}

        def convert(obj):
            """
            Recursive helper function to convert an object into its serialized form.
            """
            # Primitive types
            if obj is None or type(obj) in (
                int, str, float, bool
            ):
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
                return {"$ref": memo[identity]}

            # Assign internal id for the object
            reference = f"obj{len(memo) + 1}"
            memo[identity] = reference

            # Lists
            if isinstance(obj, list):
                return {
                    "$id": reference,
                    "$type": "list",
                    "items": [
                        convert(x) for x in obj
                    ]
                }

            # Queues (deques)
            if isinstance(obj, deque):
                return {
                    "$id": reference,
                    "$type": "deque",
                    "items": [
                        convert(x) for x in obj
                    ]
                }

            # Dictionaries
            if isinstance(obj, dict):
                return {
                    "$id": reference,
                    "$type": "dict",
                    "items": [
                        [convert(k), convert(v)]
                        for k, v in obj.items()
                    ]
                }

            # Personalized (custom) objects
            classes = type(obj)
            name = (
                classes.__module__ + "." + classes.__qualname__
            )

            if self.classes.get(name) is not classes:
                raise TypeError(
                    f"not registered class: {name}"
                )

            return {
                "$id": reference,
                "$type": "object",
                "class": name,
                "attributes": {
                    k: convert(v)
                    for k, v in vars(obj).items()
                }
            }

        return convert(obj)

    def deserialize(self, data):
        """
        Deserializes a JSON-compatible dictionary format back into a Python object.

        Args:
            data: The serialized data to reconstruct.

        Returns:
            The reconstructed Python object.
        """
        memo = {}

        def rebuild(element):
            """
            Recursive helper function to rebuild an object from its serialized form.
            """
            # Primitive types
            if not isinstance(element, dict):
                return element

            # Reference to an existing object (handling circular references)
            if "$ref" in element:
                return memo[element["$ref"]]

            type = element["$type"]

            # Dates
            if type == "datetime":
                return datetime.fromisoformat(
                    element["value"]
                )

            # Lists and queues
            if type in ("list", "deque"):
                obj = [] if type == "list" else deque()

                memo[element["$id"]] = obj

                for item in element["items"]:
                    obj.append(rebuild(item))

                return obj

            # Dictionaries
            if type == "dict":
                obj = {}
                memo[element["$id"]] = obj

                for key, value in element["items"]:
                    obj[rebuild(key)] = (
                        rebuild(value)
                    )

                return obj

            # Personalized (custom) objects
            if type == "object":
                classes = self.classes[element["class"]]

                # Create the empty instance without calling __init__
                obj = object.__new__(classes)

                # Register it before building its attributes to handle circular dependencies
                memo[element["$id"]] = obj

                for name, value in (
                    element["attributes"].items()
                ):
                    setattr(
                        obj,
                        name,
                        rebuild(value)
                    )

                return obj

            raise ValueError(
                f"Unknown type: {type}"
            )

        return rebuild(data)
    
    def save(self, scenario, path):
        """
        Serializes an object and saves it to a JSON file.

        Args:
            scenario: The object to serialize and save.
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

    def load(self, path):
        """
        Loads JSON data from a file and deserializes it back into a Python object.

        Args:
            path (str): The file path to load the JSON data from.

        Returns:
            The deserialized Python object.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.deserialize(data)
        return self.deserializar(data)