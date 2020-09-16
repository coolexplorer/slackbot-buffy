import os

from config.jira_config import JiraConfig
from config.kubernetes_config import KubernetesConfig


class Configuration:
    def __init__(self):
        self.jira = JiraConfig()
        self.kubernetes = KubernetesConfig()

    def read_env(self):
        self.kubernetes.config_type = os.environ.get('K8S_CONFIG_TYPE', 'FILE')                # ['FILE', 'IN_CLUSTER']

