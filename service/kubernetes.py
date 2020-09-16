import json
import logging

from kubernetes import client, config

from response.kubernetes_response import KubernetesResponse

logger = logging.getLogger(__name__)


class Kubernetes:
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
        response = str_format.format('Namespace', 'Pod Ip', 'Restart', 'Pod Name')

        for i in filtered:
            restart_count = sum(map(lambda x: x.restart_count, i.status.container_statuses))
            response += str_format.format(
                i.metadata.namespace, i.status.pod_ip, restart_count, i.metadata.name
            )
        blocks = KubernetesResponse().get_k8s_response(self._make_code_block(response))
        logger.debug(blocks)
        return blocks

    def _make_code_block(self, text):
        return '```{0}```'.format(text)