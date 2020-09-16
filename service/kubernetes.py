from kubernetes import client, config


class Kubernetes:
    def __init__(self, k8s_config):
        if k8s_config.config_type == 'IN_CLUSTER':
            config.load_incluster_config()
        else:
            config.load_kube_config(k8s_config.config_path)
        self.client = client

    def get_pod_list(self):
        v1 = self.client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t\t%s\t\t%s" %
                  (i.metadata.name, i.metadata.namespace, i.status.pod_ip))
