
class BaseMessage:
    def __init__(self, text):
        self.text = text

    def parse_command(self):
        return self.text.split()
