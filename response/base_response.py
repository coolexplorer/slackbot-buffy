
class BaseResponse:
    def __init__(self):
        pass

    def get_response(self, responses):
        response = [self._get_divider_block()]

        for text in responses:
            response.append(self._get_markdown_block(self._make_code_block(text)))

        return response

    @staticmethod
    def _get_divider_block():
        return {"type": "divider"}

    @staticmethod
    def _get_markdown_block(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

    @staticmethod
    def _make_code_block(text):
        return '```{0}```'.format(text)
