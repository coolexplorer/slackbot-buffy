from service.jira import Jira
from service.kubernetes import Kubernetes


class ServiceAccounts:
    def __init__(self, config):
        self.jira = Jira(config.jira) if config.jira.address != '' else None
        self.k8s = Kubernetes(config.kubernetes)
