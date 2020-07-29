from model.base_message import BaseMessage


class AppMention(BaseMessage):
    def __init__(self, event):
        BaseMessage.__init__(event['text'])
        self.type = event['type']
        self.user = event['user']
        self.text = event['text']
        self.channel = event['channel']
        self.event_ts = event['event_ts']
        self.ts = event['ts']
