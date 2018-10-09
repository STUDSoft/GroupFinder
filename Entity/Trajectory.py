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
