class CommandLineError(Exception):
    def __init__(self):
        Exception.__init__(self)


class CommandError(Exception):
    pass


class MalformedExecutionId(CommandError):
    def __init__(self):
        CommandError.__init__(self, "malformed execution id")
