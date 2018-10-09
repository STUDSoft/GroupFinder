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

    def remove_trajectory(self, position=0):
        if position is 0:
            del self.__trajectorylist[len(self.__trajectorylist) - 1]
        else:
            del self.__trajectorylist[position]

    def __str__(self):
        stringlist = [str(e) for e in self.__trajectorylist]
        return str(self.__identifier) + ":\n  " + "\n  ".join(stringlist) + "\n"
