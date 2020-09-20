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
        self.k8s_response = K8SResponse()

    def get_pods(self, namespace=None) -> str:
        v1 = self.client.CoreV1Api()
        res = v1.list_pod_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:10}\t{1:8}\t{2:10}\t{3:10}\t{4:8}\t{5:20}\n"
        header = ['Namespace', 'Ready', 'Phase', 'Pod Ip', 'Restart', 'Name']
        response = self.make_get_pod_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_deployments(self, namespace=None):
        v1 = self.client.AppsV1Api()
        res = v1.list_deployment_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        str_format = "{0:10}\t{1:8}\t{2:10}\t{3:10}\t{4:20}\n"
        header = ['Namespace', 'Ready', 'UP-TO-DATE', 'Available', 'Name']
        response = self.make_get_deployment_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_daemon_sets(self, namespace=None):
        v1 = self.client.AppsV1Api()
        res = v1.list_daemon_set_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        logger.debug(filtered)
        str_format = "{0:10}\t{1:8}\t{2:8}\t{3:8}\t{4:8}\t{5:8}\t{6:20}\n"
        header = ['Namespace', 'Desired', 'Current', 'Ready', 'UP-TO-DATE', 'Available', 'Name']
        response = self.make_get_daemon_set_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_stateful_sets(self, namespace=None):
        v1 = self.client.AppsV1Api()
        res = v1.list_stateful_set_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        logger.debug(filtered)
        str_format = "{0:10}\t{1:8}\t{2:20}\n"
        header = ['Namespace', 'Ready', 'Name']
        response = self.make_get_stateful_set_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    def get_replica_sets(self, namespace=None):
        v1 = self.client.AppsV1Api()
        res = v1.list_replica_set_for_all_namespaces(watch=False)
        filtered = [x for x in res.items if x.metadata.namespace == namespace] if namespace is not None else res.items
        logger.debug(filtered)
        str_format = "{0:10}\t{1:8}\t{2:8}\t{3:8}\t{4:20}\n"
        header = ['Namespace', 'Desired', 'Current', 'Ready', 'Name']
        response = self.make_get_replica_set_response(filtered, str_format, header)
        blocks = self.k8s_response.get_k8s_response(response)
        return blocks

    @staticmethod
    def make_get_pod_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            restart_count = sum(map(lambda x: x.restart_count, item.status.container_statuses))
            ready_count = sum(map(lambda x: 1 if x.ready is True else 0, item.status.container_statuses))
            response[block_index] += str_format.format(
                item.metadata.namespace, f"{ready_count}/{len(item.status.container_statuses)}",
                item.status.phase, item.status.pod_ip, restart_count, item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_deployment_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                item.metadata.namespace, f"{item.status.ready_replicas}/{item.status.replicas}",
                item.status.updated_replicas, item.status.available_replicas, item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_daemon_set_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            logger.debug(str_format)

            if item.status.desired_number_scheduled != 0:
                response[block_index] += str_format.format(
                    item.metadata.namespace, item.status.desired_number_scheduled, item.status.current_number_scheduled,
                    item.status.number_ready, item.status.updated_number_scheduled, item.status.number_available,
                    item.metadata.name
                )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_stateful_set_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                item.metadata.namespace, f"{item.status.ready_replicas}/{item.status.replicas}",
                item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_replica_set_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            logger.debug(str_format)

            if item.status.replicas != 0:
                response[block_index] += str_format.format(
                    item.metadata.namespace, item.status.replicas, item.status.available_replicas,
                    item.status.ready_replicas, item.metadata.name
                )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response
