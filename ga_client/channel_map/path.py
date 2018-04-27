from channel import ChannelI
from channel import PausableI
from channel import Channel
from channel import Station
from goless import go
from copy import copy

class Connection(PausableI):
    """ Represents an edge in the channel graph. Stores a reference
    to the origin channel and multiple channel destinations. """

    def __init__(self, origin, id, destinations=[]):
        self.__pause = False
        self.__origin = origin
        self.__destinations = copy(destinations)
        self.__id = id

    def foward(self):
        if self.__destinations:
            data = self.__origin.recieve()
            for destination in self.__destinations:
                destination.send(data)

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False

    def connect(self, channel):
        self.__destinations.append(channel)

    def disconnect(self, channel):
        self.__destinations.remove(channel)

    def print_destinations(self):
        print(self.__destinations)

class Path(ChannelI, PausableI):
    """ Represents a path of channels to traverse. """

    def __init__(self, nodes={}, bufferSize=0):
        self.__pause = False
        self.__nodes = nodes
        self.__connections = {}
        self.__first = None
        self.__last = None

    def send(self, data):
        if not self.__pause:
            self.__first.send(data)

    def recieve(self):
        if not self.__pause:
            for connection in self.__connections.values():
                go(connection.foward)
            return self.__last.recieve()

    def begin(self, id):
        self.__first = self.__nodes[id]
        self.__last = self.__nodes[id]
        if not self.__last in self.__connections:
            self.__connections[self.__last] = Connection(self.__last, id)

    def to(self, id):
        self.__connections[self.__last].connect(self.__nodes[id])
        self.__last = self.__nodes[id]
        if not self.__last in self.__connections:
            self.__connections[self.__last] = Connection(self.__last, id)

    def move(self, id):
        self.__last = self.__nodes[id]
        if not self.__last in self.__connections:
            self.__connections[self.__last] = Connection(self.__last)

    def close(self):
        raise NotImplementedError

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False
