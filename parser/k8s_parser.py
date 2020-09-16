from constant.k8s_command import k8s_commands, k8s_sub_commands


class K8sParser:
    def __init__(self, k8s, message):
        self.k8s = k8s
        self.message = message
        self.command = self.message[0].lower()
        self.sub_command = self.message[1].lower()
        self.case_name = "{0}_{1}".format(self.command, self.sub_command)

    def parse(self):
        if self.command in k8s_commands and self.sub_command in k8s_sub_commands:
            case = getattr(self, self.case_name, lambda: "case_default")
        else:
            raise Exception('Invalid Command')
        return case()

    def get_pods(self):
        return self.k8s.get_pods()
