from response.base_response import BaseResponse


class K8SResponse(BaseResponse):
    def __init__(self):
        BaseResponse.__init__(self)

    def get_k8s_response(self, responses):
        response = [self._get_divider_block()]

        for text in responses:
            response.append(self._get_markdown_block(self._make_code_block(text)))

        return response
