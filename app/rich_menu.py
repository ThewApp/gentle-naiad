import json
import logging

from app.lineapi import LineApi
from rasa.template.rich_menu import (DEFAULT_RICH_MENU_IMAGE,
                                     DEFAULT_RICH_MENU_OBJECT)

logger = logging.getLogger(__name__)


class RichMenu():
    def __init__(self, line_access_token):
        self.line_api = LineApi(line_access_token)

    def setup(self):
        for rich_menu in self.line_api.get_rich_menu_list():
            logger.debug("Deleting rich menu: " + rich_menu["richMenuId"])
            self.line_api.delete_rich_menu(rich_menu["richMenuId"])
        default_rich_menu_id = self.line_api.create_rich_menu(DEFAULT_RICH_MENU_OBJECT)
        with open(DEFAULT_RICH_MENU_IMAGE["path"], 'rb') as f:
            self.line_api.set_rich_menu_image(
                default_rich_menu_id, DEFAULT_RICH_MENU_IMAGE["type"], f)
        self.line_api.link_rich_menu_to_user("all", default_rich_menu_id)
        logger.debug("Linked default rich menu: " + default_rich_menu_id)
