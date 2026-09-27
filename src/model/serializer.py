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
