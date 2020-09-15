import os
import json
from slack import WebClient
from flask import Flask, request, make_response
from constant.event import events
from model.app_mention import AppMention
from model.message import Message
from parser.command_parser import CommandParser
from service.service_accounts import ServiceAccounts
from exception.invalid_command import InvalidCommand
import logging.config

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)

slack_bot_token = os.environ["SLACK_TOKEN"]
slack = WebClient(slack_bot_token)

k8s_config_type = os.environ["K8S_CONFIG_TYPE"]             # ['FILE', 'IN_CLUSTER']
service_accounts = ServiceAccounts(k8s_config=k8s_config_type)


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
        parser.parse_command()
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
