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
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_secret, line_access_token, on_new_message):
        self.line_secret = line_secret
        self.line_bot_api = LineBotApi(line_access_token)
        self.on_new_message = on_new_message

        super().__init__(self.line_secret)

        @self.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            out_channel = LineOutput(self.line_bot_api, event.reply_token)
            user_msg = UserMessage(event.message.text, out_channel, event.source.user_id,
                               input_channel=self.name())
            self.on_new_message(user_msg)
            self.line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=event.message.text + event.source.user_id))

    def handle(self, body, signature):
        # out_channel = LineOutput(self.line_bot_api)
        # on_new_message(UserMessage())
        super().handle(body, signature)

class LineOutput(OutputChannel):
    @classmethod
    def name(cls):
        return "line"
    
    def __init__(self, line_bot_api, reply_token):
        self.line_bot_api = line_bot_api
        self.reply_token = reply_token
    
    def send_text_message(self, recipient_id, message):
        self.line_bot_api.reply_message(
                self.reply_token, TextSendMessage(text="Rasa: " + message + " recipient_id: " + recipient_id))

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
        self.line_secret = line_secret
        self.line_access_token = line_access_token

    def blueprint(self, on_new_message):

        line_webhook = Blueprint('line_webhook', __name__)

        @line_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @line_webhook.route("/webhook", methods=['POST'])
        def webhook():
            signature = request.headers.get("X-Line-Signature") or ''
            body = request.get_data(as_text=True)
            handler = RasaLineHandler(self.line_secret, self.line_access_token, on_new_message)
            try:
                handler.handle(body, signature)
            except LineBotApiError as e:
                print("Got exception from LINE Messaging API: %s\n" % e.message)
                for m in e.error.details:
                    print("  %s: %s" % (m.property, m.message))
                print("\n")
            except InvalidSignatureError:
                abort(400)

            return "success"

        return line_webhook
