import json
import logging

from kubernetes import client, config

from response.k8s_response import K8SResponse

logger = logging.getLogger(__name__)

TEXT_LINE_LIMIT = 20

class K8SService:
    def __init__(self, k8s_config):
        if k8s_config.config_type == 'IN_CLUSTER':
            config.load_incluster_config()
        else:
            config.load_kube_config(k8s_config.config_path)
        self.client = client

    def get_pods(self, namespace=None) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_pod_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:15}\t{1:15}\t{2:10}\t{3:20}\n"
        header = ['Namespace', 'Pod Ip', 'Restart', 'Pod Name']
        response = self.make_get_response(filtered, str_format, header)
        blocks = K8SResponse().get_k8s_response(response)
        return blocks

    @staticmethod
    def make_get_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            restart_count = sum(map(lambda x: x.restart_count, item.status.container_statuses))
            response[block_index] += str_format.format(
                item.metadata.namespace, item.status.pod_ip, restart_count, item.metadata.name
            )
        logger.debug(response)
        return response
