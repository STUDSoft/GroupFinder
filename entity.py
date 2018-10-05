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


class Detection(object):
    def __init__(self, timestamp, pointlist=None):
        self.__timestamp = timestamp
        if pointlist is None:
            self.__pointlist = []
        else:
            self.__pointlist = pointlist

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_pointlist(self):
        return self.__pointlist

    def set_pointlist(self, pointlist):
        self.__pointlist = pointlist

    def add_point(self, point):
        self.__pointlist.append(point)

    def remove_point(self, position=0):
        if position is 0:
            del self.__pointlist[len(self.__pointlist) - 1]
        else:
            del self.__pointlist[position]

    def __str__(self):
        stringlist = [str(e) for e in self.__pointlist]
        return str(self.__timestamp) + ":\n    " + "\n    ".join(stringlist)


class User(object):
    def __init__(self, identifier, detectionlist=None):
        self.__identifier = identifier
        if detectionlist is None:
            self.__detectionlist = []
        else:
            self.__detectionlist = detectionlist

    def set_identifier(self, identifier):
        self.__identifier = identifier

    def get_identifier(self):
        return self.__identifier

    def set_detectionlist(self, detectionlist):
        self.__detectionlist = detectionlist

    def get_detectionlist(self):
        return self.__detectionlist

    def add_detection(self, detection):
        self.__detectionlist.append(detection)

    def remove_detection(self, position=0):
        if position is 0:
            del self.__detectionlist[len(self.__detectionlist) - 1]
        else:
            del self.__detectionlist[position]

    def __str__(self):
        stringlist = [str(e) for e in self.__detectionlist]
        return str(self.__identifier) + ":\n  " + "\n  ".join(stringlist) + "\n"
