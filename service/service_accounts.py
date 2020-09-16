from service.jira import Jira
from service.kubernetes import Kubernetes


class ServiceAccounts:
    def __init__(self, config):
        self.jira = Jira(config.jira)
        self.k8s = Kubernetes(config.kubernetes)
