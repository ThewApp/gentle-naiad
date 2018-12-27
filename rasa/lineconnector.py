from rasa_core.channels import UserMessage, CollectingOutputChannel, InputChannel
import requests
from flask import Blueprint, request, jsonify, abort
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage
)

import logging

logger = logging.getLogger(__name__)


class RasaLineHandler():
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, webhook, line_api, on_new_message):
        self.webhook = webhook
        self.line_api = line_api
        self.on_new_message = on_new_message

        @self.webhook.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            out_channel = LineOutput(self.line_api, event.reply_token)
            user_msg = UserMessage(event.message.text, out_channel, event.source.user_id,
                                   input_channel=self.name())
            user_msg.event = event
            self.on_new_message(user_msg)
            out_channel.send_reply()

    def handle(self, body, signature):
        self.webhook.handle(body, signature)


class LineApi():
    def __init__(self, access_token):
        self.headers = {
            "Authorization": "Bearer " + access_token
        }
        self.line_endpoint = "https://api.line.me/v2/bot/message"

    def post(self, url, data):
        response = requests.post(self.line_endpoint + url, data, headers=self.headers)
        self.check_error(response)
        return response

    def check_error(self, response):
        if 200 <= response.status_code < 300:
            pass
        else:
            logger.error('{0}: status_code={1}, error_response={2}'.format(
                self.__class__.__name__, response.status_code, response.json()))


class LineOutput(CollectingOutputChannel):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_api, reply_token):
        self.line_api = line_api
        self.reply_token = reply_token
        super().__init__()

    def send_reply(self):
        if self.messages:
            # Filter out internal keys
            internal_keys = ['recipient_id']
            messages = [{key: message[key] for key in message if key not in internal_keys}
                        for message in self.messages]
            data = {
                'replyToken': self.reply_token,
                'messages': messages
            }
            return self.line_api.post("/reply", data)


class LineInput(InputChannel):
    """LINE input channel implementation. Based on the HTTPInputChannel."""

    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_secret, line_access_token):
        # type: (Text, Text, Text) -> None
        """Create a line input channel.
        Needs a couple of settings to properly authenticate and validate
        messages.
        Args:
            line_secret: Line Signature validation
            line_access_token: Access token
        """
        self.webhook = WebhookHandler(line_secret)
        self.line_api = LineApi(line_access_token)

    def blueprint(self, on_new_message):

        line_webhook = Blueprint('line_webhook', __name__)

        @line_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @line_webhook.route("/webhook", methods=['POST'])
        def webhook():
            signature = request.headers.get("X-Line-Signature") or ''
            body = request.get_data(as_text=True)
            handler = RasaLineHandler(
                self.webhook, self.line_api, on_new_message)
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)

            return "success"

        return line_webhook
