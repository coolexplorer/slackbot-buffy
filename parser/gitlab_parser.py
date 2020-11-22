import logging

from constant.gitlab_command import gitlab_commands
from constant.gitlab_command import gitlab_sub_commands

logger = logging.getLogger(__name__)


class GitlabParser:
    def __init__(self, gitlab, message):
        self.gitlab = gitlab
        self.message = message
        self.command = self.message[0].lower()
        self.gitlab_command = self.message[1].lower()
        self.gitlab_sub_command = self.message[2].lower() if len(message) > 3 else "func"
        self.params = self.message[3:]
        self.case_name = "{0}_{1}".format(self.gitlab_command, self.gitlab_sub_command)
        self.param_func_name = "_check_{0}_params".format(self.gitlab_command)

    def parse(self):
        sub_commands = gitlab_sub_commands.get(self.gitlab_command, ["func"])
        if self.gitlab_command in gitlab_commands and self.gitlab_sub_command in sub_commands:
            case = getattr(self, self.case_name, lambda: "case_default")
        else:
            logger.error(f'Invalid Command: {self.case_name}')
            raise Exception('Invalid Command')
        check_params = getattr(self, self.param_func_name, lambda: "_check_params")
        check_params()
        return case()

    def _check_project_params(self):
        if '-k' in self.params:
            index = self.params.index('-k')
            self.keyword = self.params[index + 1]

    def _check_pipeline_params(self):
        if '-pid' in self.params:
            index = self.params.index('-pid')
            self.project_id = self.params[index + 1]
        if '-ref' in self.params:
            index = self.params.index('-ref')
            self.ref = self.params[index + 1]
        if '-var' in self.params:
            index = self.params.index('-var')
            self.ref = self.params[index + 1]

    def _check_variable_params(self):
        if '-pid' in self.params:
            index = self.params.index('-pid')
            self.project_id = self.params[index + 1]

    def _check_params(self):
        pass

    def help_func(self):
        return self.gitlab.get_help()

    def project_list(self):
        return self.gitlab.get_project_list()

    def project_search(self):
        return self.gitlab.search_projects(self.keyword)

    def pipeline_list(self):
        return self.gitlab.get_pipeline_list(self.project_id)

    def pipeline_variable(self):
        return self.gitlab.get_pipeline_variables(self.project_id)

    def pipeline_create(self):
        return self.gitlab.create_pipeline(self.project_id)

    def variable_list(self):
        return self.gitlab.get_variable_list(self.project_id)
