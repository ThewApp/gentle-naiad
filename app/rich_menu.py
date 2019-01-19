import json
import logging

from app.lineapi import LineApi
from rasa.template.rich_menu import (
    RICH_MENU_DEFAULT_OBJECT, RICH_MENU_DEFAULT_IMAGE,
    RICH_MENU_THINGS_OBJECT, RICH_MENU_THINGS_IMAGE
)

logger = logging.getLogger(__name__)


class RichMenu():
    def __init__(self, line_access_token):
        self.line_api = LineApi(line_access_token)

    def setup(self):
        # Delete all old rich menus
        for rich_menu in self.line_api.get_rich_menu_list():
            logger.debug("Deleting rich menu: " + rich_menu["richMenuId"])
            self.line_api.delete_rich_menu(rich_menu["richMenuId"])
        # Setup new default rich menu
        default_rich_menu_id = self.line_api.create_rich_menu(RICH_MENU_DEFAULT_OBJECT)
        with open(RICH_MENU_DEFAULT_IMAGE["path"], 'rb') as f:
            self.line_api.set_rich_menu_image(
                default_rich_menu_id, RICH_MENU_DEFAULT_IMAGE["type"], f)
        self.line_api.link_rich_menu_to_user("all", default_rich_menu_id)
        logger.debug("Setup and linked default rich menu: " + default_rich_menu_id)
        # Setup new things rich menu
        things_rich_menu_id = self.line_api.create_rich_menu(RICH_MENU_THINGS_OBJECT)
        with open(RICH_MENU_THINGS_IMAGE["path"], 'rb') as f:
            self.line_api.set_rich_menu_image(
                things_rich_menu_id, RICH_MENU_THINGS_IMAGE["type"], f)
        logger.debug("Setup things rich menu: " + things_rich_menu_id)
