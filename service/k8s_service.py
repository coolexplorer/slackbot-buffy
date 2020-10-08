import json
import logging

from kubernetes import client, config

from response.k8s_response import K8SResponse

logger = logging.getLogger(__name__)


class K8SService:
    def __init__(self, k8s_config):
        if k8s_config.config_type == 'IN_CLUSTER':
            config.load_incluster_config()
        else:
            config.load_kube_config(k8s_config.config_path)
        self.client = client
        self.k8s_response = K8SResponse()

    def get_pods(self, namespace=None) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_pod_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:12}\t{1:8}\t{2:10}\t{3:10}\t{4:8}\t{5:20}\n"
        header = ['Namespace', 'Ready', 'Phase', 'Pod Ip', 'Restart', 'Name']
        response = self.k8s_response.make_get_pod_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_deployments(self, namespace=None) -> str:
        v1 = self.client.AppsV1Api()
        res = v1.list_deployment_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:12}\t{1:8}\t{2:8}\t{3:8}\t{4:20}\n"
        header = ['Namespace', 'Ready', 'UP-TO-DATE', 'Available', 'Name']
        response = self.k8s_response.make_get_deployment_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_daemon_sets(self, namespace=None) -> str:
        v1 = self.client.AppsV1Api()
        res = v1.list_daemon_set_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        logger.debug(filtered)
        str_format = "{0:12}\t{1:8}\t{2:8}\t{3:8}\t{4:8}\t{5:8}\t{6:20}\n"
        header = ['Namespace', 'Desired', 'Current', 'Ready', 'UP-TO-DATE', 'Available', 'Name']
        response = self.k8s_response.make_get_daemon_set_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_stateful_sets(self, namespace=None) -> str:
        v1 = self.client.AppsV1Api()
        res = v1.list_stateful_set_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        logger.debug(filtered)
        str_format = "{0:12}\t{1:8}\t{2:20}\n"
        header = ['Namespace', 'Ready', 'Name']
        response = self.k8s_response.make_get_stateful_set_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_replica_sets(self, namespace=None) -> str:
        v1 = self.client.AppsV1Api()
        res = v1.list_replica_set_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        logger.debug(filtered)
        str_format = "{0:12}\t{1:8}\t{2:8}\t{3:8}\t{4:20}\n"
        header = ['Namespace', 'Desired', 'Current', 'Ready', 'Name']
        response = self.k8s_response.make_get_replica_set_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_namespaces(self) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_namespace(watch=False)
        str_format = "{0:10}\t{1:20}\n"
        header = ['Status', 'Name']
        response = self.k8s_response.make_get_namespace_response(res.items, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        logger.debug(res.items)
        return blocks

    def get_config_map(self, namespace=None) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_config_map_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:12}\t{1:3}\t{2:20}\n"
        header = ['Namespace', 'Data', 'Name']
        response = self.k8s_response.make_get_config_map_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_secret(self, namespace=None) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_secret_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:12}\t{1:3}\t{2:20}\n"
        header = ['Namespace', 'Data', 'Type', 'Name']
        response = self.k8s_response.make_get_secret_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_nodes(self) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_node(watch=False)
        str_format = "{0:12}\t{1:10}\t{2:10}\t{3:20}\n"
        header = ['Status', 'Roles', 'Version', 'Name']
        response = self.k8s_response.make_get_node_response(res.items, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks
