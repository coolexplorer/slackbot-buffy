from jira import JIRA


class Jira:
    def __init__(self):
        self.client = JIRA('https://jaas.ea.com', basic_auth=('seunkim@ea.com', 'yeojinsihoodahee'))

    def get_projects(self):
        projects = self.client.projects()
        keys = sorted([project.key for project in projects])[2:5]
        return projects

    def get_boards(self, name):
        boards = self.client.boards()
        return list(filter(lambda x: name in x.name, boards))

