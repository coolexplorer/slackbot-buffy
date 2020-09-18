import importlib
import logging
from util.string_util import StringUtil
from constant.command import commands

logger = logging.getLogger(__name__)


class CommandParser:
    def __init__(self, service_accounts, message):
        self.service_accounts = service_accounts
        self.message = message
        self.command = self.message[0].lower()
        self.parser_name = self.command + '_parser'
        self.case_name = 'case_' + self.command
        logger.info(f"message {message}")
        logger.info(f'parser_name : {self.parser_name}, case_name : {self.case_name}')

    def parse_command(self):
        if self.command in commands:
            case = getattr(self, self.case_name, lambda: "case_default")
        else:
            logger.info(f"{self.command}")
            raise Exception('Invalid Command')
        return case()

    def case_jira(self):
        module = importlib.import_module(f'parser.{self.parser_name}')
        class_ = getattr(module, StringUtil.snake_to_camel(self.parser_name))
        instance = class_(self.service_accounts.jira, self.message)
        return instance.parse()

    def case_k8s(self):
        module = importlib.import_module(f'parser.{self.parser_name}')
        class_ = getattr(module, StringUtil.snake_to_camel(self.parser_name))
        instance = class_(self.service_accounts.k8s, self.message)
        return instance.parse()

    def case_default(self):
        logger.error("case_default")
        pass



