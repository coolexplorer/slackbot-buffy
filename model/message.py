from model.base_message import BaseMessage


class Message(BaseMessage):
    def __init__(self, event):
        BaseMessage.__init__(self, event.get('text'))
        self.type = event.get('type')
        self.sub_type = event.get('subtype')
        self.user = event.get('user')
        self.text = event.get('text')
        self.channel = event.get('channel')
        self.ts = event.get('ts')
