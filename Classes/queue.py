from heapq import heappush, heappop, heapify


class PriorityQueue(object):
    __REMOVED = '<removed-item>'

    def __init__(self):
        self.__pq = []
        self.__entry_finder = {}

    def push(self, item, priority=0):
        'Add a new task or update the priority of an existing task'
        if item in self.__entry_finder:
            self.remove(item)
        entry = [priority, item]
        self.__entry_finder[item] = entry
        heappush(self.__pq, entry)

    def remove(self, item):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.__entry_finder.pop(item)
        entry[-1] = self.__REMOVED

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.__pq:
            priority, item = heappop(self.__pq)
            if item is not self.__REMOVED:
                del self.__entry_finder[item]
                return item
        return KeyError("Empty queue")

    def empty(self):
        if len(self.__entry_finder) > 0:
            return False
        else:
            return True
