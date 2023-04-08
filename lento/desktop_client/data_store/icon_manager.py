import logging
from uuid import UUID

from grabicon import FaviconGrabber
from PySide6.QtGui import QIcon

from lento.config import Config

from .card_items import BlockItemType

"""
Manages icon path
"""


class IconManager:
    def __init__(self):
        icons = {}
        for child in Config.ICON_PATH.iterdir():
            if child.is_file():
                blockitem_id = child.stem
                icons[blockitem_id] = QIcon(str(child))

        self.icons = icons

    def load_icon(
        self, blockitem_id: UUID, blockitem_path: str, item_type: BlockItemType
    ):
        try:
            res = self.icons[blockitem_id]
        except KeyError:
            match item_type:
                case BlockItemType.WEBSITE:
                    res = self._get_favicon(blockitem_path, blockitem_id)
                case BlockItemType.APP:
                    res = self._get_app_icon(blockitem_path, blockitem_id)
            self.icons[blockitem_id] = QIcon(str(res))
        return res

    def _get_favicon(self, website_url, blockitem_id):
        try:
            grabber = FaviconGrabber()
            favicon = grabber.grab(website_url)[0]
        except Exception:
            logging.info("Failed to load favicon for {}".format(website_url))
            return ""

        icon_path = Config.ICON_PATH / f"{blockitem_id}.{favicon.extension}"
        logging.info("Saving favicon for {} at {}".format(website_url, icon_path))
        icon_path.write_bytes(favicon.data)
        return icon_path

    def _get_app_icon(self, app_id, blockitem):
        pass


def save_icon(image, icon_name):
    """
    Save icon image with the specified name

    Parameters:
    image: a PIL.Image object
    icon_name: the name of the icon to save
    """
    rgb_im = image.convert("RGB")
    icon_path = str(Config.ICON_PATH / (icon_name + ".jpg"))
    rgb_im.save(icon_path)

    return icon_path


def cleanup_saved_icon(cards):
    """
    Deletes all unused icon files
    """
    pass
    # logging.info("Deleting unused icon images at {}".format(Config.ICON_PATH))
    # file_names = os.listdir(Config.ICON_PATH)
    # used_icons = set()

    # # find the list of icon paths currently used
    # for card_id in cards:
    #     card_item = cards[card_id]
    #     for label in card_item.block_items:
    #         item = card_item.block_items.get(label)
    #         if item.icon_path is not None:
    #             used_icons.add(item.icon_path)

    # logging.info("Using the following icon paths: {}".format(used_icons))

    # # delete the icon files that are not currently used
    # for file_name in file_names:
    #     file_path = os.path.join(str(Config.ICON_PATH), file_name)
    #     if os.path.isfile(file_path):
    #         if file_path not in used_icons:
    #             logging.info("Removing file {}".format(file_path))
    #             os.remove(file_path)
