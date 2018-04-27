from channel import ChannelI
from channel import PausableI
from channel import Channel
from channel import Station
from path import Path

class ChannelMap(PausableI):
    def __init__(self):
        self.__pause = False
        self.__nodes = {}
        self.__paths = {}

    def start(self):
        pass

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False

    def channel(self, id, bufferSize=0):
        self.__nodes[id] = Channel(bufferSize)
        return self.__nodes[id]

    def station(self, id, function, bufferSize=0):
        self.__nodes[id] = Station(function, bufferSize)
        return self.__nodes[id]

    def path(self, id, bufferSize=0):
        self.__paths[id] = Path(self.__nodes, bufferSize)
        return self.__paths[id]
