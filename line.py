from rasa_core.channels import UserMessage, OutputChannel, InputChannel
from flask import Blueprint, request, jsonify, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage)

class RasaLineHandler(WebhookHandler):
    def __init__(self, line_secret):
        super().__init__(line_secret)

    def handle(self, body, signature, on_new_message):
        super().handle(body, signature)


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
        # self.line_secret = line_secret
        # self.line_access_token = line_access_token
        self.line_bot_api = LineBotApi(line_access_token)
        self.handler = RasaLineHandler(line_secret)

        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            self.line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=event.message.text + event.source.user_id))

    def blueprint(self, on_new_message):

        line_webhook = Blueprint('line_webhook', __name__)

        @line_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @line_webhook.route("/webhook", methods=['POST'])
        def webhook():
            signature = request.headers.get("X-Line-Signature") or ''
            body = request.get_data(as_text=True)
            try:
                self.handler.handle(body, signature, on_new_message)
            except LineBotApiError as e:
                print("Got exception from LINE Messaging API: %s\n" % e.message)
                for m in e.error.details:
                    print("  %s: %s" % (m.property, m.message))
                print("\n")
            except InvalidSignatureError:
                abort(400)

            return "success"

        return line_webhook
