import os

from config.jira_config import JiraConfig
from config.k8s_config import K8SConfig


class Configuration:
    def __init__(self):
        self.jira = JiraConfig()
        self.kubernetes = K8SConfig()

    def read_env(self):
        self.jira.address = os.environ.get('JIRA_HOST', '')
        self.jira.basic_auth_user = os.environ.get('JIRA_BASIC_AUTH_USER', '')
        self.jira.basic_auth_pass = os.environ.get('JIRA_BASIC_AUTH_PASS', '')
        self.kubernetes.config_type = os.environ.get('K8S_CONFIG_TYPE', 'FILE')                # ['FILE', 'IN_CLUSTER']
        self.kubernetes.config_path = os.environ.get('K8S_CONFIG_PATH', '~/.kube/config')

