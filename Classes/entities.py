class Point(object):
    def __init__(self, coordinates, timestamp=None):
        self.__coordinates = coordinates
        self.__timestamp = timestamp

    def get_coordinates(self):
        return self.__coordinates

    def set_coordinates(self, coordinates):
        self.__coordinates = coordinates

    def get_latitude(self):
        return self.__coordinates.get_latitude()

    def set_latitude(self, latitude):
        self.__coordinates.set_latitude(latitude)

    def get_longitude(self):
        return self.__coordinates.get_longitude()

    def set_longitude(self, longitude):
        self.__coordinates.set_longitude(longitude)

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def __repr__(self):
        return str(self.__coordinates.get_latitude()) + ", " + str(self.__coordinates.get_longitude()) + " on " + str(
            self.__timestamp)


class Trajectory(object):
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
    def __init__(self, identifier, trajectorylist=None):
        self.__identifier = identifier
        if trajectorylist is None:
            self.__trajectorylist = []
        else:
            self.__trajectorylist = trajectorylist

    def set_identifier(self, identifier):
        self.__identifier = identifier

    def get_identifier(self):
        return self.__identifier

    def set_trajectorylist(self, trajectorylist):
        self.__trajectorylist = trajectorylist

    def get_trajectorylist(self):
        return self.__trajectorylist

    def add_trajectory(self, trajectory):
        self.__trajectorylist.append(trajectory)

    def get_trajectory(self, position):
        return self.__trajectorylist[position]

    def remove_trajectory(self, position=0):
        if position is 0:
            del self.__trajectorylist[len(self.__trajectorylist) - 1]
        else:
            del self.__trajectorylist[position]

    def __str__(self):
        stringlist = [str(e) for e in self.__trajectorylist]
        return str(self.__identifier) + ":\n  " + "\n  ".join(stringlist) + "\n"


class StayPoint(Point):
    def __init__(self, coordinates, user_identifier, arv_time=None, leav_time=None):
        self.__user_identifier = user_identifier
        self.__arv_time = arv_time
        self.__leav_time = leav_time
        super(StayPoint, self).__init__(coordinates)

    def get_user_identifier(self):
        return self.__user_identifier

    def set_user_identifier(self, user_identifier):
        self.__user_identifier = user_identifier

    def get_arv_time(self):
        return self.__arv_time

    def set_arv_time(self, arv_time):
        self.__arv_time = arv_time

    def get_leav_time(self):
        return self.__leav_time

    def set_leav_time(self, leav_time):
        self.__leav_time = leav_time

    def __repr__(self):
        return str(self.__user_identifier) + " at " + str(
            super(StayPoint, self).get_coordinates().get_latitude()) + ", " \
               + str(super(StayPoint, self).get_coordinates().get_longitude()) \
               + " arv at " + str(self.__arv_time) + " left at " + str(self.__leav_time)
