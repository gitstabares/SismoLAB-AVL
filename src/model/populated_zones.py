import json

from src.model.point import Point


class PopulatedZones:

    def __init__(self, file_path):
        self.__map_size = 1000
        self.__zone_size = 100

        self.__map = [
            [False for _ in range(self.__map_size)]
            for _ in range(self.__map_size)
        ]

        self.__populated_zones = []
        self.__populated_zone_set = set()

        self.__load_zones(file_path)

    def __load_zones(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for zone in data["populated_zones"]:
            x = zone["x"]
            y = zone["y"]

            point = Point(x, y)

            self.__populated_zones.append(point)
            self.__populated_zone_set.add((x, y))

            self.__mark_zone(x, y)

    def __mark_zone(self, x, y):
        for i in range(x, x + self.__zone_size):
            for j in range(y, y + self.__zone_size):
                self.__map[i][j] = True

    def __is_populated_zone(self, x, y):
        return (x, y) in self.__populated_zone_set

    def contains(self, point):
        x_zone = point.x - point.x % self.__zone_size
        y_zone = point.y - point.y % self.__zone_size

        x_zone = int(x_zone)
        y_zone = int(y_zone)

        if self.__is_populated_zone(x_zone, y_zone):
            return True

        return False

    def get_populated_zones(self):
        return self.__populated_zones