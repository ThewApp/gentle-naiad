import json
import logging

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

from rasa.template.rich_menu import (DEFAULT_RICH_MENU_IMAGE,
                                     DEFAULT_RICH_MENU_OBJECT)

logger = logging.getLogger(__name__)


class RichMenu():
    def __init__(self, line_access_token):
        self.line_api = LineBotApi(line_access_token)

    def setup(self):
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
