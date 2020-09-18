
class BaseMessage:
    def __init__(self, text):
        self.text = text

    def parse_message(self, is_mention):
        if is_mention is True:
            return self.text.split()[1:]
        else:
            return self.text.split()
