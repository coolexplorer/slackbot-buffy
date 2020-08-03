import importlib
import logging
from util.string_util import StringUtil
import constant.command

logger = logging.getLogger(__name__)


class CommandParser:
    def __init__(self, message):
        self.message = message
        self.command = self.message[0]
        self.parser_name = self.command + '_parser'
        self.case_name = 'case_' + self.command
        logger.debug(f'parser_name : {self.parser_name}, case_name : {self.case_name}')

    def parse_command(self):
        case = getattr(self, self.case_name, lambda: "case_default")
        return case()

    def case_jira(self):
        module = importlib.import_module(f'parser.{self.parser_name}')
        class_ = getattr(module, StringUtil.snake_to_camel(self.parser_name))
        instance = class_(self.message)
        instance.parse()

    def case_default(self):
        raise Exception('Invalid command')



