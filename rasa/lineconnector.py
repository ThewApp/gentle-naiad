import json
import logging

from flask import Blueprint, jsonify
from rasa_core.channels import (CollectingOutputChannel, InputChannel,
                                UserMessage)

from app.lineapi import LineApi, WebhookHandler

logger = logging.getLogger(__name__)


class RasaLineHandler(WebhookHandler):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, channel_secret, line_api: LineApi):
        self.line_api = line_api
        super().__init__(channel_secret)

    def handle_text(self, event):
        logger.info("Line Text: %s from %s",
                    event["message"]["text"], event["source"]["userId"])
        out_channel = LineOutput(self.line_api, event["replyToken"])
        user_msg = UserMessage(
            event["message"]["text"],
            out_channel,
            event["source"]["userId"],
            input_channel=self.name()
        )
        self.on_new_message(user_msg)
        out_channel.send_reply()

    def handle_postback(self, event):
        logger.info("Line Postback: %s from %s",
                    event["postback"]["data"], event["source"]["userId"])
        out_channel = LineOutput(self.line_api, event["replyToken"])
        user_msg = UserMessage(
            event["postback"]["data"],
            out_channel,
            event["source"]["userId"],
            input_channel=self.name()
        )
        self.on_new_message(user_msg)
        out_channel.send_reply()

    def handle_follow(self, event):
        logger.info("Line Follow from %s", event["source"]["userId"])
        out_channel = LineOutput(self.line_api, event["replyToken"])
        user_msg = UserMessage(
            "/follow_event",
            out_channel,
            event["source"]["userId"],
            input_channel=self.name()
        )
        self.on_new_message(user_msg)
        out_channel.send_reply()

    def handle_unfollow(self, event):
        logger.info("Line Unfollow from %s", event["source"]["userId"])
        user_msg = UserMessage(
            "/unfollow_event",
            None,
            event["source"]["userId"],
            input_channel=self.name()
        )
        self.on_new_message(user_msg)


RECIPIENT_ID = "recipient_id"


class LineOutput(CollectingOutputChannel):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_api: LineApi, reply_token=None):
        self.line_api = line_api
        self.reply_token = reply_token
        super().__init__()

    def add_message(self, recipient_id, message):
        message[RECIPIENT_ID] = recipient_id
        self.messages.append(message)

    def send_reply(self):
        if self.messages:
            # Filter out internal keys
            internal_keys = [RECIPIENT_ID]
            messages = [{key: message[key] for key in message if key not in internal_keys}
                        for message in self.messages]

            data = {
                'replyToken': self.reply_token,
                'messages': messages
            }

            logger.debug("Sending reply... %s", data)

            return self.line_api.reply_message(data)

    def send_push(self):
        if self.messages:
            to = self.messages[0][RECIPIENT_ID]
            # Filter out internal keys
            internal_keys = [RECIPIENT_ID]
            messages = [{key: message[key] for key in message if key not in internal_keys}
                        for message in self.messages]

            data = {
                'to': to,
                'messages': messages
            }

            logger.debug("Sending push... %s", data)

            return self.line_api.push_message(data)

    def clear_messages(self):
        self.messages = []


class LineInput(InputChannel):
    """LINE input channel implementation. Based on the HTTPInputChannel."""

    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_secret: str, line_access_token: str):
        # type: (Text, Text, Text) -> None
        """Create a line input channel.
        Needs a couple of settings to properly authenticate and validate
        messages.
        Args:
            line_secret: Line Signature validation
            line_access_token: Access token
        """
        self.line_api = LineApi(line_access_token)
        self.handler = RasaLineHandler(line_secret, self.line_api)

    def blueprint(self, on_new_message):

        line_webhook = Blueprint('line_webhook', __name__)

        @line_webhook.route("/", methods=['GET'])
        # pylint: disable=unused-variable
        def health():
            return jsonify({"status": "ok"})

        @line_webhook.route("/webhook", methods=['POST'])
        # pylint: disable=unused-variable
        def webhook():
            self.handler.handle_webhook(on_new_message)

            return "success"

        return line_webhook
