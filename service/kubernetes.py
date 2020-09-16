from kubernetes import client, config


class Kubernetes:
    def __init__(self, kubernetes_config):
        if kubernetes_config.config_type == 'IN_CLUSTER':
            config.load_incluster_config()
        else:
            config.load_kube_config(kubernetes_config.config_path)
        self.client = client
