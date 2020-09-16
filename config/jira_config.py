
class JiraConfig:
    def __init__(self, address='https://jaas.ea.com', basic_auth_user='', basic_auth_pass=''):
        self.address = address
        self.basic_auth_user = basic_auth_user
        self.basic_auth_pwd = basic_auth_pass

    def __str__(self):
        return f"address: {self.address}, basic_auth_user: {self.basic_auth_user}"
