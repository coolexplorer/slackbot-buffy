from kubernetes import client, config


class Kubernetes:
    def __init__(self, k8s_config):
        if k8s_config == "IN_CLUSTER":
            config.load_incluster_config()
        else:
            config.load_kube_config()
        self.client = client
