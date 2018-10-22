from Classes.entities import StayPoint
from Classes.entities import Cluster

class Coordinates(object):
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def set_longitude(self, longitude):
        self.__longitude = longitude


class StayPointClust(StayPoint):
    def __init__(self, sp, reach_dist=None, core_dist=None, processed=False, cluster_id=None):
        self.__reach_dist = reach_dist
        self.__core_dist = core_dist
        self.__processed = processed
        self.__cluster_id = cluster_id
        super(StayPointClust, self).__init__(sp.get_coordinates(), sp.get_arv_time(), sp.get_leav_time())

    def get_reach_dist(self):
        return self.__reach_dist

    def set_reach_dist(self, reach_dist):
        self.__reach_dist = reach_dist

    def get_core_dist(self):
        return self.__core_dist

    def set_core_dist(self, core_dist):
        self.__core_dist = core_dist

    def get_processed(self):
        return self.__processed

    def set_processed(self, processed):
        self.__processed = processed

    def get_cluster_id(self):
        return self.__cluster_id

    def set_cluster_id(self, cluster_id):
        self.__cluster_id = cluster_id

    def __repr__(self):
        if self.__cluster_id is Cluster.NOISE:
            return str(self.get_coordinates().get_latitude()) + ", " + str(
                self.get_coordinates().get_longitude()) + " in noise, core dist " + str(
                self.__core_dist) + ", reach dist " + str(self.__reach_dist)
        else:
            return str(self.get_coordinates().get_latitude()) + ", " + str(
                self.get_coordinates().get_longitude()) + " in cluster " + str(self.__cluster_id) + ", core dist " + str(
                self.__core_dist) + ", reach dist " + str(self.__reach_dist)
