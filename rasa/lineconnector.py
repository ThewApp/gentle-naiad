import json
import logging

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (AudioSendMessage, BaseSize, ImagemapAction,
                            ImagemapArea, ImagemapSendMessage,
                            ImageSendMessage, LocationSendMessage,
                            MessageEvent, StickerSendMessage,
                            TemplateSendMessage, TextMessage, TextSendMessage,
                            VideoSendMessage)

from flask import Blueprint, abort, jsonify, request
from rasa_core.channels import (CollectingOutputChannel, InputChannel,
                                UserMessage)

logger = logging.getLogger(__name__)


class RasaLineHandler(WebhookHandler):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, channel_secret, line_api):
        self.line_api = line_api
        super().__init__(channel_secret)

        self.add(MessageEvent, message=TextMessage)(self.handle_text_message)

    def handle_webhook(self, on_new_message):
        self.on_new_message = on_new_message
        signature = request.headers.get("X-Line-Signature") or ''
        body = request.get_data(as_text=True)
        logger.info("Handling... %s", body)
        self.handle(body, signature)

    def handle_text_message(self, event):
        out_channel = LineOutput(self.line_api, event.reply_token)
        user_msg = UserMessage(event.message.text, out_channel, event.source.user_id,
                               input_channel=self.name())
        user_msg.event = event
        self.on_new_message(user_msg)
        out_channel.send_reply()


class LineOutput(CollectingOutputChannel):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_api, reply_token):
        self.line_api = line_api
        self.reply_token = reply_token
        super().__init__()

    def add_reply(self, recipient_id, message):
        message['recipient_id'] = recipient_id
        self.messages.append(message)

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

            logger.info("Sending reply... %s", data)

            return self.line_api._post(
                '/v2/bot/message/reply', data=json.dumps(data)
            )


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
        self.line_api = LineBotApi(line_access_token)
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
            try:
                self.handler.handle_webhook(on_new_message)
            except LineBotApiError as e:
                print("Got exception from LINE Messaging API: %s\n" % e.message)
                for m in e.error.details:
                    print("  %s: %s" % (m.property, m.message))
                print("\n")
            except InvalidSignatureError:
                abort(400)

            return "success"

        return line_webhook
