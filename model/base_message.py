
class BaseMessage:
    def __init__(self, text):
        self.text = text

    def parse_message(self):
        return self.text.split()
