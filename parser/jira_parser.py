import logging

logger = logging.getLogger(__name__)


class JiraParser:
    def __init__(self, jira, message):
        self.jira = jira
        self.message = message

    def parse(self):
        logger.debug(self.jira.get_boards("QEAP"))


