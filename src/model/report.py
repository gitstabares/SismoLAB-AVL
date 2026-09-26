from src.model import Point
from datetime import datetime as dt

class Report:
    def __init__(self, id, magnitude, deepness, x, y, date, review, origin_station):
        self.__id = self.__set_id(id)
        self.__magnitude = self.__set_magnitude(magnitude)
        self.__deepness = self.__set_deepness(deepness)
        self.__epicenter = self.__set_epicenter(x,y)
        self.__date = self.__set_date(date)
        self.__review = self.__set_review(review)
        self.__origin_station = origin_station

    def get_id(self):
        return self.__id

    def __set_id(self, id):
        self.__id = max(1, min(999999, int(id)))

    def get_magnitude(self):
        return self.__magnitude

    def __set_magnitude(self, magnitude):
        self.__magnitude = max(-2, min(10, round(magnitude,1)))
    
    def get_deepness(self):
        return self.__deepness

    def __set_deepness(self, deepness):
        self.__deepness = max(0, min(700, round(deepness,1)))
    
    def get_epicenter(self):
        return self.__epicenter

    def __set_epicenter(self, x, y):
        self.__epicenter = Point(x, y)
   
    def get_date(self):
        return self.__date

    def __set_date(self, date):
        self.__date = dt.fromisoformat(date)

    def get_review(self):
        return self.__review

    def __set_review(self, review):
        self.__review = max(0, int(review))
    
    def get_origin_station(self):
        return self.__origin_station
    


