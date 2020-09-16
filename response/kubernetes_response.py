from response.base_response import BaseResponse


class KubernetesResponse(BaseResponse):
    def __init__(self):
        BaseResponse.__init__(self)

    def get_k8s_response(self, text):
        return {
            "blocks": [
                self._get_divider_block(),
                self._get_markdown_block(text)
            ]
        }
