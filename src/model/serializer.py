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

            # 1. Tipos primitivos
            if obj is None or type(obj) in (
                int, str, float, bool
            ):
                return obj

            # 2. Fechas
            if isinstance(obj, datetime):
                return {
                    "$type": "datetime",
                    "value": obj.isoformat()
                }

            # 3. Comprobar referencias anteriores
            identity = id(obj)

            if identity in memo:
                return {"$ref": memo[identity]}

            # 4. Asignar identificador interno
            reference = f"obj{len(memo) + 1}"
            memo[identity] = reference

            # 5. Listas
            if isinstance(obj, list):
                return {
                    "$id": reference,
                    "$type": "list",
                    "items": [
                        convert(x) for x in obj
                    ]
                }

            # 6. Colas
            if isinstance(obj, deque):
                return {
                    "$id": reference,
                    "$type": "deque",
                    "items": [
                        convert(x) for x in obj
                    ]
                }

            # 7. Diccionarios
            if isinstance(obj, dict):
                return {
                    "$id": reference,
                    "$type": "dict",
                    "items": [
                        [convert(k), convert(v)]
                        for k, v in obj.items()
                    ]
                }

            # 8. Objetos personalizados
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
