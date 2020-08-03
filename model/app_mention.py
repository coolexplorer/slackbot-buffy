from model.base_message import BaseMessage


class AppMention(BaseMessage):
    def __init__(self, event):
        BaseMessage.__init__(self, event.get('text'))
        self.type = event.get('type')
        self.user = event.get('user')
        self.text = event.get('text')
        self.channel = event.get('channel')
        self.event_ts = event.get('event_ts')
        self.ts = event.get('ts')
