import gitlab

from response.gitlab_response import GitlabResponse


class GitlabService:
    def __init__(self, gitlab_config):
        self.gitlab = gitlab.Gitlab(gitlab_config.host, private_token=gitlab_config.private_token)
        self.gitlab_response = GitlabResponse()

    def get_project_list(self):
        projects = self.gitlab.projects.list(owned=True)
        str_format = "{0:8}\t{1:12}\n"
        header = ['ID', 'Project']
        response = self.gitlab_response.make_get_projects_response(projects, str_format, header)
        blocks = self.gitlab_response.get_gitlab_response(response)
        return blocks

    def search_projects(self, keyword):
        projects = self.gitlab.projects.list(owned=True, search=keyword)
        str_format = "{0:8}\t{1:12}\n"
        header = ['ID', 'Project']
        response = self.gitlab_response.make_get_projects_response(projects, str_format, header)
        blocks = self.gitlab_response.get_gitlab_response(response)
        return blocks

    def get_pipeline_list(self, pid):
        pipelines = self.gitlab.projects.get(pid).pipelines.list()
        str_format = "{0:8}\t{1:8}\t{2:10}\n"
        header = ['ID', 'status', 'ref']
        response = self.gitlab_response.make_get_pipelines_response(pipelines, str_format, header)
        blocks = self.gitlab_response.get_gitlab_response(response)
        return blocks

    def get_pipeline_variables(self, pid):
        pipelines = self.gitlab.projects.get(pid).pipelines.list()
        variables = []
        if len(pipelines) > 0:
            variables = pipelines[0].variables.list()
        str_format = "{0:18}\t{1:12}\t{2:12}\n"
        header = ['key', 'variable_type', 'value']
        response = self.gitlab_response.make_get_pipeline_variables_response(variables, str_format, header)
        blocks = self.gitlab_response.get_gitlab_response(response)
        return blocks

    def get_variable_list(self, pid):
        variables = self.gitlab.projects.get(pid).variables.list()
        str_format = "{0:18}\t{1:12}\t{2:12}\n"
        header = ['key', 'variable_type', 'value']
        response = self.gitlab_response.make_get_variables_response(variables, str_format, header)
        blocks = self.gitlab_response.get_gitlab_response(response)
        return blocks
