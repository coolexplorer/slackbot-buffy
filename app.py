import os
import json
from slack import WebClient
from flask import Flask, request, make_response
from config.cofiguration import Configuration
from constant.event import events
from model.app_mention import AppMention
from model.message import Message
from parser.command_parser import CommandParser
from service.service_accounts import ServiceAccounts
from exception.invalid_command import InvalidCommand
import logging.config

# log
logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# web server
app = Flask(__name__)

# slack
slack_bot_token = os.environ.get('SLACK_TOKEN', 'xoxb-3339495132-1270691607044-oXckdW4MCYu3HyTWIf4KKXhV')
slack = WebClient(token=slack_bot_token, run_async=True)

# buffy configuration
config = Configuration()
config.read_env()
service_accounts = ServiceAccounts(config)


async def event_handler(event_type, event_data):
    message = None
    if event_type in events:
        if event_type == "app_mention":
            message = AppMention(event_data['event'])
        elif event_type == "message":
            message = Message(event_data["event"])

        commands = message.parse_message()
        logger.debug(f"message {commands}")
        _parse_command(message, commands)
        args = [
            "Successfully sent the mention.",
            200
        ]
    else:
        args = [
            f"[{event_type}] Cannot find the event handler",
            200,
            {"X-Slack-No-Retry": 1}
        ]
    return make_response(*args)


def _parse_command(message, commands):
    try:
        parser = CommandParser(service_accounts, commands)
        blocks = parser.parse_command()
        logger.debug(f"response message: {blocks}")

        slack.chat_postMessage(channel=message.channel, blocks=blocks)
    except InvalidCommand as e:
        logger.error(e)
        slack.chat_postMessage(channel=message.channel, text=e)


@app.route("/slack", methods=["GET", "POST"])
def event_api():
    event_data = json.loads(request.data)
    if "challenge" in event_data:
        return make_response(event_data["challenge"], 200, {"content_type": "application/json"})
    if "event" in event_data:
        event_type = event_data["event"]["type"]
        return event_handler(event_type, event_data)
    return make_response("No match the event type.", 404, {"X-Slack-No-Retry": 1})


@app.route("/ping", methods=["GET"])
def health_check_api():
    return make_response("pong", 200, {"content_type": "application/json"})


if __name__ == '__main__':
    logger.debug(f'Jira Configuration {config.jira}')
    logger.debug(f'Kubernetes Configuration {config.kubernetes}')
    app.run('0.0.0.0', port=8080)
