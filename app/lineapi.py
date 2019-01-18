import json
import logging

import requests

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
