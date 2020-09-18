from model.base_message import BaseMessage


class Message(BaseMessage):
    def __init__(self, event):
        BaseMessage.__init__(self, event.get('text'))
        self.type = event.get('type')
        self.user = event.get('user')
        self.team = event.get('team')
        self.text = event.get('text')
        self.channel = event.get('channel')
        self.ts = event.get('ts')
        self.bot_id = None

