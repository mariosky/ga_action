class Logger:
    """ Logs messages if the verbose mode is active. """
    def __init__(self, verbose):
        self.verbose = verbose

    def log(self, message):
        if (self.verbose):
            print(message)
