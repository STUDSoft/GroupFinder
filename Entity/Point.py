class Point(object):
    def __init__(self, latitude, longitude, timestamp):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__timestamp = timestamp

    def get_latitude(self):
        return self.__latitude

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def get_longitude(self):
        return self.__longitude

    def set_longitude(self, longitude):
        self.__longitude = longitude

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def __repr__(self):
        return str(self.__latitude) + ", " + str(self.__longitude) + " on " + str(self.__timestamp)
