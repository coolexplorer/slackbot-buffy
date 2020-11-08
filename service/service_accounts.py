from service.gitlab_service import GitlabService
from service.jira_service import JiraService
from service.k8s_service import K8SService


class ServiceAccounts:
    def __init__(self, config):
        self.jira = JiraService(config.jira) if config.jira.host != '' else None
        self.k8s = K8SService(config.kubernetes)
        self.gitlab = GitlabService(config.gitlab) if config.gitlab.host != '' else None
