from goless import chan

class ChannelI:
    """ Defines the methods of a channel. """

    def send(self, data):
        raise NotImplementedError

    def recieve(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

class PausableI:
    """ Defines a pause and resume method. """

    def pause(self):
        raise NotImplementedError

    def resume(self):
        raise NotImplementedError

class Channel(ChannelI, PausableI):
    """ Simple channel class. It uses the decorator pattern. """

    def __init__(self, bufferSize=0):
        self.__pause = False
        self.__channel = chan(bufferSize)

    def send(self, data):
        if not self.__pause:
            self.__channel.send(data)

    def recieve(self):
        if not self.__pause:
            return self.__channel.recv()

    def close(self):
        self.__channel.close()

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False

class Station(ChannelI, PausableI):
    """ More complex channel class. When recieved it performs some operation
    on the channels data. Uses the decorator pattern. """

    def __init__(self, function, bufferSize=0):
        self.__pause = False
        self.__function = function
        self.__channel = chan(bufferSize)

    def send(self, data):
        if not self.__pause:
            self.__channel.send(data)

    def recieve(self):
        if not self.__pause:
            return self.__function(self.__channel.recv())

    def close(self):
        self.__channel.close()

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False
