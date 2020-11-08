
class JiraConfig:
    def __init__(self, host='https://jaas.ea.com', basic_auth_user='', basic_auth_pass=''):
        self.host = host
        self.basic_auth_user = basic_auth_user
        self.basic_auth_pwd = basic_auth_pass

    def __str__(self):
        return f"address: {self.host}, basic_auth_user: {self.basic_auth_user}"
