from model.base_message import BaseMessage


class Message(BaseMessage):
    def __init__(self, event):
        BaseMessage.__init__(event['text'])
        self.type = event['type']
        self.sub_type = event['subtype']
        self.user = event['user']
        self.text = event['text']
        self.channel = event['channel']
        self.ts = event['ts']