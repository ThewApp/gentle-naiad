import json
import logging

import requests

logger = logging.getLogger(__name__)


class LineApi():
    def __init__(self, access_token):
        self.headers = {
            "Authorization": "Bearer " + access_token,
            'Content-Type': 'application/json'
        }
        self.line_endpoint = "https://api.line.me/v2/bot/message"

    def _post(self, url, data, timeout):
        response = requests.post(
            self.line_endpoint + url, data=json.dumps(data), headers=self.headers, timeout=timeout)
        self.check_error(response)
        return response

    def reply_message(self, reply_token: str, messages, timeout=None):

        data = {
            'replyToken': reply_token,
            'messages': messages
        }

        self._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )

    def check_error(self, response):
        if 200 <= response.status_code < 300:
            pass
        else:
            logger.error('{0}: status_code={1}, error_response={2}'.format(
                self.__class__.__name__, response.status_code, response.json()))
