from jira import JIRA


class JiraService:
    def __init__(self, jira_config):
        self.client = JIRA(jira_config.address, basic_auth=(jira_config.basic_auth_user, jira_config.basic_auth_pass))

    def get_projects(self):
        projects = self.client.projects()
        keys = sorted([project.key for project in projects])[2:5]
        return projects

    def get_boards(self, name):
        boards = self.client.boards()
        return list(filter(lambda x: name in x.name, boards))

