class CommandLineError(Exception):
    def __init__(self):
        Exception.__init__(self)


class CommandError(Exception):
    pass
