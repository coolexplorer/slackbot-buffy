import logging

from response.base_response import BaseResponse

logger = logging.getLogger(__name__)
TEXT_LINE_LIMIT = 20


class GitlabResponse(BaseResponse):
    def __init__(self):
        BaseResponse.__init__(self)

    def get_gitlab_response(self, responses):
        response = [self._get_divider_block()]

        for text in responses:
            response.append(self._get_markdown_block(self._make_code_block(text)))

        return response

    @staticmethod
    def make_get_projects_response(projects, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, project in enumerate(projects):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                project.id, project.name
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_pipelines_response(pipelines, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, pipeline in enumerate(pipelines):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                pipeline.id, pipeline.status, pipeline.ref
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_pipeline_variables_response(variables, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, variable in enumerate(variables):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                variable.key, variable.variable_type, variable.value
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response

    @staticmethod
    def make_get_variables_response(variables, str_format, header):
        header = str_format.format(*header)
        response = []
        block_index = -1

        for i, variable in enumerate(variables):
            if i % TEXT_LINE_LIMIT == 0:
                response.append(header)
                block_index += 1

            response[block_index] += str_format.format(
                variable.key, variable.variable_type, variable.value
            )

        if len(response) == 0:
            response.append("No data")

        logger.debug(response)
        return response
