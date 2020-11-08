
class GitlabConfig:
    def __init__(self, host='', private_token=''):
        self.host = host
        self.private_token = private_token

    def __str__(self):
        return f"Gitlab host: {self.host}"
