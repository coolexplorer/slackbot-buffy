import logging.config
import os
import re

from slack import RTMClient
from slack.errors import SlackApiError

from config.cofiguration import Configuration
from exception.invalid_command import InvalidCommand
from model.message import Message
from parser.command_parser import CommandParser
from service.service_accounts import ServiceAccounts

# log
logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# slack
slack_bot_token = os.environ.get('SLACK_TOKEN', '')
rtm_client = RTMClient(token=slack_bot_token)

# buffy configuration
config = Configuration()
config.read_env()
service_accounts = ServiceAccounts(config)


@RTMClient.run_on(event='message')
def message_event_handler(**payload):
    logger.debug(f"payload : {payload}")
    data = payload['data']
    sub_type = data.get('subtype', None)
    if sub_type is not None:
        return

    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'text' in data:
        message = Message(data)
        is_mention, message.bot_id = check_mention(message.text)
        commands = message.parse_message(is_mention)
        logger.debug(f"message {commands}")
        _parse_command(web_client, message, commands)


def check_mention(text):
    pattern = re.compile('<@([a-zA-z0-9]*)>')
    match = pattern.match(text)
    if match is not None:
        return [True, match.group(1)]
    else:
        return [False, None]


def _parse_command(web_client, message, commands):
    try:
        parser = CommandParser(service_accounts, commands)
        blocks = parser.parse_command()
        logger.debug(f"response message: {blocks}")

        web_client.chat_postMessage(channel=message.channel, blocks=blocks, thread_ts=message.ts)
    except InvalidCommand as e:
        logger.error(e)
        web_client.chat_postMessage(channel=message.channel, text=e)
    except SlackApiError as e:
        logger.error(f"Got an error: {e.response['error']}")


if __name__ == '__main__':
    logger.info(f'Jira Configuration {config.jira}')
    logger.info(f'Kubernetes Configuration {config.kubernetes}')
    logger.info(f'RTM Client is started....')
    rtm_client.start()
