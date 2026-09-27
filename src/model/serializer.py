import json
from collections import deque
from datetime import datetime


class Serializer:

    def __init__(self):
        self.classes = {}

    def register(self, classes):
        name = classes.__module__ + "." + classes.__qualname__
        self.classes[name] = classes

    def serialize(self, obj):
        memo = {}

        def convert(obj):

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

            # Check previous references
            identity = id(obj)

            if identity in memo:
                return {"$ref": memo[identity]}

            # Assign internal id
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

            # Queues
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

            # Personalized objects
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
        memo = {}

        def rebuild(element):

            # Primitive types
            if not isinstance(element, dict):
                return element

            # Reference to an existing object
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

            # Personalized objects
            if type == "object":
                classes = self.classes[element["class"]]

                # Create the empty instance
                obj = object.__new__(classes)

                # Register it before building its attributes
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

        data = self.serializar(scenario)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
                allow_nan=False
            )

    def load(self, path):

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.deserializar(data)