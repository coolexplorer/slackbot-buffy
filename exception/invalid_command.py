

class InvalidCommand(Exception):
    def __str__(self):
        return "This command is not supported. "
