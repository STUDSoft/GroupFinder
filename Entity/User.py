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
