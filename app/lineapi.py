import base64
import hashlib
import hmac
import json
import logging

import requests
from flask import abort, request

from app.database import users, things

logger = logging.getLogger(__name__)


class LineApi():
    def __init__(self, channel_access_token: str, timeout: float = 5.0):
        self.endpoint = "https://api.line.me"
        self.headers = {
            'Authorization': 'Bearer ' + channel_access_token
        }
        self.timeout = timeout

    def reply_message(self, data: dict, **kwargs):
        return self._post('/v2/bot/message/reply', json=data, **kwargs)

    def push_message(self, data: dict, **kwargs):
        return self._post('/v2/bot/message/push', json=data, **kwargs)

    def multicast(self, data: dict, **kwargs):
        return self._post('/v2/bot/message/multicast', json=data, **kwargs)

    def create_rich_menu(self, rich_menu: dict, **kwargs):

        response = self._post('/v2/bot/richmenu', json=rich_menu, **kwargs)

        return response.json().get('richMenuId')

    def delete_rich_menu(self, rich_menu_id: str, **kwargs):
        return self._delete(
            '/v2/bot/richmenu/{rich_menu_id}'.format(
                rich_menu_id=rich_menu_id),
            **kwargs
        )

    def get_rich_menu_id_of_user(self, user_id: str, **kwargs):
        response = self._get(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            **kwargs
        )

        return response.json().get('richMenuId')

    def link_rich_menu_to_user(self, user_id: str, rich_menu_id: str, **kwargs):
        return self._post(
            '/v2/bot/user/{user_id}/richmenu/{rich_menu_id}'.format(
                user_id=user_id,
                rich_menu_id=rich_menu_id
            ),
            **kwargs
        )

    def unlink_rich_menu_from_user(self, user_id: str, **kwargs):
        return self._delete(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            **kwargs
        )

    def set_rich_menu_image(self, rich_menu_id: str, content_type: str, content, **kwargs):
        return self._post(
            '/v2/bot/richmenu/{rich_menu_id}/content'.format(
                rich_menu_id=rich_menu_id),
            data=content,
            headers={'Content-Type': content_type},
            **kwargs
        )

    def get_rich_menu_list(self, **kwargs):
        response = self._get('/v2/bot/richmenu/list', **kwargs)

        return response.json().get('richmenus')

    def _get(self, path, headers={}, timeout=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        url = self.endpoint + path

        headers.update(self.headers)

        response = requests.get(
            url, headers=headers, timeout=timeout, **kwargs
        )

        self.__check_error(response)
        return response

    def _post(self, path, headers={}, timeout=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        url = self.endpoint + path

        headers.update(self.headers)

        response = requests.post(
            url, headers=headers, timeout=timeout, **kwargs
        )

        self.__check_error(response)
        return response

    def _delete(self, path, headers={}, timeout=None, **kwargs):
        url = self.endpoint + path

        headers.update(self.headers)

        response = requests.delete(
            url, headers=headers, timeout=timeout, **kwargs
        )

        self.__check_error(response)
        return response

    @staticmethod
    def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            text = response.text
            logger.error("Got exception from LINE Messaging API: %s\n" % text)


class WebhookHandler():
    def __init__(self, channel_secret):
        self.channel_secret = channel_secret

    def signature_validate(self, body, signature):
        gen_signature = hmac.new(
            self.channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).digest()

        return hmac.compare_digest(
            signature.encode('utf-8'), base64.b64encode(gen_signature)
        )

    def handle_webhook(self, on_new_message):
        self.on_new_message = on_new_message
        signature = request.headers.get("X-Line-Signature") or ''
        body = request.get_data(as_text=True)
        logger.debug("Handling... %s", body)

        if not self.signature_validate(body, signature):
            abort(400)

        body_json = json.loads(body)
        for event in body_json['events']:
            users.userUttered(event["source"]["userId"][-32:])
            event_type = event['type']
            if event_type == 'message':
                self.handle_message(event)
            elif event_type == 'follow':
                self.handle_follow(event)
            elif event_type == 'unfollow':
                self.handle_unfollow(event)
            elif event_type == 'join':
                self.handle_join(event)
            elif event_type == 'leave':
                self.handle_leave(event)
            elif event_type == 'memberJoined':
                self.handle_member_joined(event)
            elif event_type == 'memberLeft':
                self.handle_member_left(event)
            elif event_type == 'postback':
                self.handle_postback(event)
            elif event_type == 'beacon':
                self.handle_beacon(event)
            elif event_type == 'accountLink':
                self.handle_account_link(event)
            elif event_type == 'things':
                self.handle_things(event)
            else:
                logger.warn('Unknown event type. type=' + event_type)

    def handle_message(self, event):
        message_type = event["message"].get("type", None)
        if message_type == "text":
            self.handle_text(event)
        elif message_type == "image":
            self.handle_image(event)
        elif message_type == "video":
            self.handle_video(event)
        elif message_type == "audio":
            self.handle_audio(event)
        elif message_type == "file":
            self.handle_file(event)
        elif message_type == "location":
            self.handle_location(event)
        elif message_type == "sticker":
            self.handle_sticker(event)
        else:
            logger.warn('Unknown message type. type=' + message_type)

    def handle_text(self, event):
        logger.debug(
            "No text message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_image(self, event):
        logger.debug(
            "No image message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_video(self, event):
        logger.debug(
            "No video message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_audio(self, event):
        logger.debug(
            "No audio message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_file(self, event):
        logger.debug(
            "No file message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_location(self, event):
        logger.debug(
            "No location message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_sticker(self, event):
        logger.debug(
            "No sticker message handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_follow(self, event):
        logger.debug(
            "No follow handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_unfollow(self, event):
        logger.debug(
            "No unfollow handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_join(self, event):
        logger.debug("No join handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_leave(self, event):
        logger.debug(
            "No leave handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_member_joined(self, event):
        logger.debug(
            "No memberJoined handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_member_left(self, event):
        logger.debug(
            "No memberLeft handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_postback(self, event):
        logger.debug(
            "No postback handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_beacon(self, event):
        logger.debug(
            "No beacon handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_account_link(self, event):
        logger.debug(
            "No accountLink handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_things(self, event):
        things_type = event["things"].get("type", None)
        if things_type == "link":
            things.updateHas(event["source"]["userId"][-32:], True)
            self.handle_things_link(event)
        elif things_type == "unlink":
            things.updateHas(event["source"]["userId"][-32:], False)
            self.handle_things_unlink(event)
        else:
            logger.warn('Unknown things type. type=' + things_type)

    def handle_things_link(self, event):
        logger.debug(
            "No things link handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_things_unlink(self, event):
        logger.debug(
            "No things unlink handler implemented. Calling default handler...")
        self.handle_default(event)

    def handle_default(self, event):
        logger.debug('No handler of ' +
                     event["type"] + ' and no default handler')
