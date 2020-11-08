import os

from config.gitlab_config import GitlabConfig
from config.jira_config import JiraConfig
from config.k8s_config import K8SConfig


class Configuration:
    def __init__(self):
        self.jira = JiraConfig()
        self.kubernetes = K8SConfig()
        self.gitlab = GitlabConfig()

    def read_env(self):
        self._read_jira_env()
        self._read_k8s_env()
        self._read_gitlab_env()

    def _read_jira_env(self):
        self.jira.host = os.environ.get('JIRA_HOST', '')
        self.jira.basic_auth_user = os.environ.get('JIRA_BASIC_AUTH_USER', '')
        self.jira.basic_auth_pass = os.environ.get('JIRA_BASIC_AUTH_PASS', '')

    def _read_k8s_env(self):
        self.kubernetes.config_type = os.environ.get('K8S_CONFIG_TYPE', 'FILE')  # ['FILE', 'IN_CLUSTER']
        self.kubernetes.config_path = os.environ.get('K8S_CONFIG_PATH', '~/.kube/config')

    def _read_gitlab_env(self):
        self.gitlab.host = os.environ.get('GITLAB_HOST', '')
        self.gitlab.private_token = os.environ.get('GITLAB_PRIVATE_TOKEN', '')
        self.gitlab.username = os.environ.get('GITLAB_USERNAME', '')
        self.gitlab.username = os.environ.get('GITLAB_PASSWORD', '')
