
class KubernetesConfig:
    def __init__(self, config_type='FILE', config_path='~/.kube/config'):
        self.config_type = config_type
        self.config_path = config_path
