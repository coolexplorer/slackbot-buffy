from service.jira import Jira
from service.kubernetes import Kubernetes


class ServiceAccounts:
    def __init__(self, k8s_config):
        self.jira = Jira()
        self.k8s = Kubernetes(k8s_config)
