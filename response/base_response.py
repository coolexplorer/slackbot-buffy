
class BaseChat:
    def __init__(self):
        pass

    @staticmethod
    def _get_markdown_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}}
        ]
