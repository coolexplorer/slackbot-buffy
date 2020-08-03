from jira import JIRA


class JiraClient:
    def __init__(self):
        self.jira_client = JIRA('https://jaas.ea.com', basic_auth=('seunkim@ea.com', 'yeojinsihoodahee'))

    def get_projects(self):
        projects = self.jira_client.projects()
        keys = sorted([project.key for project in projects])[2:5]
        return projects
