import logging

from constant.k8s_command import k8s_commands, k8s_sub_commands

logger = logging.getLogger(__name__)


class K8SParser:
    def __init__(self, k8s, message):
        self.k8s = k8s
        self.message = message
        self.command = self.message[0].lower()
        self.k8s_command = self.message[1].lower()
        self.k8s_sub_command = self.message[2].lower()
        self.params = self.message[3:]
        self.case_name = "{0}_{1}".format(self.k8s_command, self.k8s_sub_command)
        self.namespace = None

    def parse(self):
        if self.k8s_command in k8s_commands and self.k8s_sub_command in k8s_sub_commands:
            case = getattr(self, self.case_name, lambda: "case_default")
        else:
            logger.error(f'Invalid Command: {self.case_name}')
            raise Exception('Invalid Command')
        self._check_params()
        return case()

    def _check_params(self):
        if '-n' in self.params:
            index = self.params.index('-n')
            self.namespace = self.params[index + 1]

    def get_pods(self):
        return self.k8s.get_pods(self.namespace)

    def get_deploys(self):
        return self.k8s.get_deployments(self.namespace)

    def get_daemons(self):
        return self.k8s.get_daemon_sets(self.namespace)

    def get_states(self):
        return self.k8s.get_stateful_sets(self.namespace)

    def get_replicas(self):
        return self.k8s.get_replica_sets(self.namespace)

    def get_ns(self):
        return self.k8s.get_namespaces()

    def get_configmap(self):
        return self.k8s.get_config_map(self.namespace)

    def get_secret(self):
        return self.k8s.get_secret(self.namespace)

    def get_nodes(self):
        return self.k8s.get_nodes()