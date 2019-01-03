import json
import logging

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    FollowEvent, UnfollowEvent, MessageEvent, PostbackEvent,
    TextMessage
)

from flask import Blueprint, abort, jsonify, request
from rasa_core.channels import (
    CollectingOutputChannel, InputChannel, UserMessage
)
from rasa.template.rich_menu import DEFAULT_RICH_MENU_OBJECT, DEFAULT_RICH_MENU_IMAGE

logger = logging.getLogger(__name__)


class RasaLineHandler(WebhookHandler):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, channel_secret, line_api):
        self.line_api = line_api
        super().__init__(channel_secret)

        self.setupRichMenu()

        self.add(MessageEvent, message=TextMessage)(self.handle_text_message)
        self.add(PostbackEvent)(self.handle_postback_event)
        self.add(FollowEvent)(self.handle_follow_event)
        self.add(UnfollowEvent)(self.handle_unfollow_event)

    def setupRichMenu(self):
        for rich_menu in self.line_api.get_rich_menu_list():
            try:
                logger.debug("Deleting rich menu: " + rich_menu.rich_menu_id)
                self.line_api.delete_rich_menu(rich_menu.rich_menu_id)
            except LineBotApiError as e:
                logger.error(e.status_code, e.error.message, e.error.details)
        default_rich_menu_object = DEFAULT_RICH_MENU_OBJECT
        default_rich_menu_id = self.line_api._post(
            '/v2/bot/richmenu', data=json.dumps(default_rich_menu_object)
        ).json.get('richMenuId')
        with open(DEFAULT_RICH_MENU_IMAGE["path"], 'rb') as f:
            self.line_api.set_rich_menu_image(
                default_rich_menu_id, DEFAULT_RICH_MENU_IMAGE["type"], f)
        self.line_api.link_rich_menu_to_user("all", default_rich_menu_id)
        logger.debug("Linked default rich menu: " + default_rich_menu_id)

    def handle_webhook(self, on_new_message):
        self.on_new_message = on_new_message
        signature = request.headers.get("X-Line-Signature") or ''
        body = request.get_data(as_text=True)
        logger.debug("Handling... %s", body)
        self.handle(body, signature)

    def handle_text_message(self, event):
        logger.info("Line Text: %s from %s",
                    event.message.text, event.source.user_id)
        out_channel = LineOutput(self.line_api, event.reply_token)
        user_msg = UserMessage(
            event.message.text,
            out_channel,
            event.source.user_id,
            input_channel=self.name()
        )
        self.on_new_message(user_msg)
        out_channel.send_reply()

    def handle_postback_event(self, event):
        logger.info("Line Postback: %s from %s",
                    event.postback.data, event.source.user_id)
        out_channel = LineOutput(self.line_api, event.reply_token)
        user_msg = UserMessage(
            event.postback.data,
            out_channel,
            event.source.user_id,
            input_channel=self.name()
        )
        self.on_new_message(user_msg)
        out_channel.send_reply()

    def handle_follow_event(self, event):
        logger.info("Line Follow from %s", event.source.user_id)
        out_channel = LineOutput(self.line_api, event.reply_token)
        user_msg = UserMessage(
            "/follow_event",
            out_channel,
            event.source.user_id,
            input_channel=self.name()
        )
        self.on_new_message(user_msg)
        out_channel.send_reply()

    def handle_unfollow_event(self, event):
        logger.info("Line Unfollow from %s", event.source.user_id)
        user_msg = UserMessage(
            "/unfollow_event",
            None,
            event.source.user_id,
            input_channel=self.name()
        )
        self.on_new_message(user_msg)


RECIPIENT_ID = "recipient_id"


class LineOutput(CollectingOutputChannel):
    @classmethod
    def name(cls):
        return "line"

    def __init__(self, line_api, reply_token=None):
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

            self.messages = []

            return self.line_api._post(
                '/v2/bot/message/reply', data=json.dumps(data)
            )

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

            self.messages

            return self.line_api._post(
                '/v2/bot/message/push', data=json.dumps(data)
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
                logger.error(
                    "Got exception from LINE Messaging API: %s\n" % e.message)
                for m in e.error.details:
                    logger.error("  %s: %s" % (m.property, m.message))
            except InvalidSignatureError:
                abort(400)

            return "success"

        return line_webhook
