import os

from config.jira_config import JiraConfig
from config.kubernetes_config import KubernetesConfig


class Configuration:
    def __init__(self):
        self.jira = JiraConfig()
        self.kubernetes = KubernetesConfig()

    def read_env(self):
        self.jira.address = os.environ.get('JIRA_HOST', 'https://jaas.ea.com')
        self.jira.basic_auth_user = os.environ.get('JIRA_BASIC_AUTH_NAME', 'seunkim@ea.com')
        self.jira.basic_auth_pass = os.environ.get('JIRA_BASIC_AUTH_PASS', 'yeojinsihoodahee')
        self.kubernetes.config_type = os.environ.get('K8S_CONFIG_TYPE', 'FILE')                # ['FILE', 'IN_CLUSTER']
        self.kubernetes.config_path = os.environ.get('K8S_CONFIG_PATH', '~/.kube/config')

