import logging
from service.jira import JiraClient

logger = logging.getLogger(__name__)


class JiraParser:
    def __init__(self, message):
        self.message = message
        self.jira_client = JiraClient()

    def parse(self):
        logger.debug(self.jira_client.get_projects())


