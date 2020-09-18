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
        return case()

    def _check_params(self):
        if '-n' in self.params:
            index = self.params.index('-n')
            self.namespace = self.params[index + 1]

    def get_pods(self):
        self._check_params()
        return self.k8s.get_pods(self.namespace)
