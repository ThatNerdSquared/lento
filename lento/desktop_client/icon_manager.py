import os
import logging
from lento.config import Config
from grabicon import FaviconGrabber

"""
Manages icon path
"""


def load_favicon(website_url):
    """
    Loads favicon based on provided website URL
    """
    # load favicons
    try:
        grabber = FaviconGrabber()
        favicons = grabber.grab(website_url)
    except Exception:
        logging.info("Failed to load favicon for {}".format(website_url))
        return ""

    logging.info("Loaded favicons for {}: {}".format(website_url, favicons))

    # save loaded favicon to file
    if len(favicons) > 0:
        icon = favicons[0]
        trimmed_url = website_url.replace("\\", "_").replace("/", "_")
        icon_path = Config.ICON_PATH / f"{trimmed_url}.{icon.extension}"

        logging.info("Saving favicon for {} at {}".format(website_url, icon_path))
        icon_path.write_bytes(icon.data)
        return str(icon_path)

    return ""


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
    logging.info("Deleting unused icon images at {}".format(Config.ICON_PATH))
    file_names = os.listdir(Config.ICON_PATH)
    used_icons = set()

    # find the list of icon paths currently used
    for card_id in cards:
        card_item = cards[card_id]
        for label in card_item.block_items:
            item = card_item.block_items.get(label)
            if item.icon_path is not None:
                used_icons.add(item.icon_path)

    logging.info("Using the following icon paths: {}".format(used_icons))

    # delete the icon files that are not currently used
    for file_name in file_names:
        file_path = os.path.join(str(Config.ICON_PATH), file_name)
        if os.path.isfile(file_path):
            if file_path not in used_icons:
                logging.info("Removing file {}".format(file_path))
                os.remove(file_path)
