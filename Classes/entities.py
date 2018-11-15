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

    def get_coord_pointlist(self):
        ptl = []
        for p in self.__pointlist:
            ptl.append((p.get_latitude(), p.get_longitude()))
        return ptl

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


class Sequence(object):
    def __init__(self, user_id=None):
        self.__nodes = []
        self.__user_id = user_id

    def has_nodes(self):
        return len(self.__nodes) != 0

    def get_nodes(self):
        return self.__nodes

    def set_nodes(self, nodes):
        self.__nodes = nodes

    def add_node(self, node):
        self.__nodes.append(node)

    def delete_node(self, node):
        self.__nodes.remove(node)

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_latest_node(self):
        return self.__nodes[len(self.__nodes) - 1]

    def __repr__(self):
        return "User " + str(self.__user_id) + " sequence:\n" + str(self.__nodes[:]) + "\n"


class Node(object):
    def __init__(self, clust_id, time_to, num_sp, leav_time):
        self.__time_to = time_to
        self.__clust_id = clust_id
        self.__num_sp = num_sp
        self.__leav_time = leav_time

    def add_staypoint(self):
        self.__num_sp += 1

    def remove_staypoint(self):
        self.__num_sp -= 1

    def get_num_staypoints(self):
        return self.__num_sp

    def set_num_staypoints(self, num_sp):
        self.__num_sp = num_sp

    def get_clust_id(self):
        return self.__clust_id

    def set_clust_id(self, clust_id):
        self.__clust_id = clust_id

    def get_time_to(self):
        return self.__time_to

    def set_time_to(self, time_to):
        self.__time_to = time_to

    def set_leav_time(self, leav_time):
        self.__leav_time = leav_time

    def get_leav_time(self):
        return self.__leav_time

    def __repr__(self):
        return "Cluster " + str(self.__clust_id) + " arv in " + str(self.get_time_to()) + " hours and left at " + str(
            self.get_leav_time()) + " for a total of " + str(self.get_num_staypoints()) + " staypoints.\n"
