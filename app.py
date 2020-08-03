from slackeventsapi import SlackEventAdapter
from slack import WebClient
import os
from model.app_mention import AppMention
from model.message import Message
from parser.command_parser import CommandParser
import logging
import logging.config

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

slack_signing_secret = os.environ["SLACK_EVENTS_TOKEN"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

slack_bot_token = os.environ["SLACK_TOKEN"]
slack_client = WebClient(slack_bot_token)


@slack_events_adapter.on("message")
def handle_message(event_data):
    message = Message(event_data["event"])
    commands = message.parse_message()
    logger.debug(f"message {commands}")
    parser = CommandParser(commands)
    parser.parse_command()


@slack_events_adapter.on("app_mention")
def handle_mention(event_data):
    app_mention = AppMention(event_data['event'])
    commands = app_mention.parse_message()
    logger.debug(f"message {commands}")
    parser = CommandParser(commands[1:])
    parser.parse_command()
    # text = "What can I do for you?"
    # slack_client.chat_postMessage(channel=app_mention.channel, text=text)


@slack_events_adapter.on("error")
def error_handler(err):
    logger.error("ERROR: " + str(err))


if __name__ == "__main__":
    slack_events_adapter.start(host='0.0.0.0', port=3000)

