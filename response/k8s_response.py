import logging

from response.base_response import BaseResponse

logger = logging.getLogger(__name__)
TEXT_LINE_LIMIT = 20


class K8SResponse(BaseResponse):
    def __init__(self):
        BaseResponse.__init__(self)

    def get_k8s_response(self, responses):
        response = [self._get_divider_block()]

        for text in responses:
            response.append(self._get_markdown_block(self._make_code_block(text)))

        return response

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

    @staticmethod
    def make_get_namespace_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                item.status.phase, item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_config_map_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                item.status.phase, len(item.data), item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_secret_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                item.metadata.namespace, len(item.data), item.type, item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_node_response(items, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, item in enumerate(items):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            role = 'master' if 'node-role.kubernetes.io/master' in item.metadata.labels.keys() else '<None>'
            kublet = [x for x in item.status.conditions if x.type == 'Ready'][0]
            status = kublet.type if kublet.status == 'True' else 'Not Ready'
            print(role, status)
            response[block_index] += str_format.format(
                status, role, item.status.node_info.kubelet_version, item.metadata.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response
