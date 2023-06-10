import logging
import os
import platform
import plistlib
import subprocess
import time
import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

import lento.desktop_client.data_store.icon_manager as IconManager
import lento.desktop_client.model.cards_management as CardsManagement
from lento.config import Config

# TODO: each block item class should generate its own serialized dict,
# this requires a restructure of lentosettings.json where we save a
# list of block item with each card instead of organizing them into
# blocked apps and websites. Move both serialization and deserialization
# code to block item


class LentoBlockItem(ABC):
    """
    Base class for any block items
    """

    def __init__(self, softblock=False, popup_item=None, allow_interval=60):
        """
        Parameters:
        softblock: whether the block item is softblocked
        popup_item: the popup item associated with the block item
        allow_interval: how long this block item will be allowed for
        """
        self.softblock = softblock
        self.popup_item = popup_item
        self.allow_interval = allow_interval
        self.icon_path = None
        self.label = None

    @abstractmethod
    def save(self, parent_card):
        """Will be implemented by child class."""

    @abstractmethod
    def delete(self, parent_card):
        """Will be implemented by child class."""

    @abstractmethod
    def print(self):
        """Will be implemented by child class."""


class LentoAppItem(LentoBlockItem):
    """
    Class containing all information of an app item
    """

    def __init__(
        self, app_path, softblock=False, popup_item=None, allow_interval=60, load=True
    ):
        """
        Parameters:
        app_path: path to app bundle/executable
        softblock: whether the block item is softblocked
        popup_item: the popup item associated with the block item
        allow_interval: how long this block item will be allowed for
        load: whether to load app info from file or not
        """
        super().__init__(
            softblock=softblock, popup_item=popup_item, allow_interval=allow_interval
        )
        self.label = Path(app_path).stem
        self.app_path = app_path
        self.app_bundle_id = None
        if load:
            self.load_app_info()

    def save(self, parent_card):
        """
        Save the app item to lento settings under a parent card item
        """
        if self.icon_path is not None and self.icon_path != "":
            im = Image.open(self.icon_path)
            self.icon_path = IconManager.save_icon(im, self.label)
        CardsManagement.save_app_item(parent_card, self)

    def delete(self, parent_card):
        """
        Delete the app item from lento settings under a parent
        card item
        """
        CardsManagement.delete_app_item(parent_card, self)

    def load_app_info(self):
        """
        Loads app info from saved metadata in app bundle
        """
        logging.info("Loading app info for {}".format(self.app_path))

        current_os = platform.system()
        if current_os == "Darwin":
            # get app bundle ID
            self.app_bundle_id = subprocess.check_output(
                ["mdls", "-name", "kMDItemCFBundleIdentifier", "-r", self.app_path]
            ).decode("utf-8")

            # determine app bundle info plist path
            if self.app_path[:14] == "/Applications/":
                self.app_path = os.path.join(
                    Config.MACOS_APPLICATION_FOLDER, Path(self.app_path).name
                )
                plist_path = Path(self.app_path, "Contents", "Info.plist")
            else:
                plist_path = Path(self.app_path, "Contents", "Info.plist")

            # load info plist and find app icon name
            logging.info("Loading app info from plist path: {}".format(plist_path))
            app_plist = plistlib.loads(plist_path.read_bytes())
            icon_name = app_plist.get("CFBundleIconFile")
            logging.info("Got icon name {} for app {}".format(icon_name, self.app_path))

            if icon_name:
                if icon_name[-5:] != ".icns":
                    icon_name = icon_name + ".icns"

                original_icon_path = Path(
                    self.app_path, "Contents", "Resources", icon_name
                )
                self.icon_path = original_icon_path

            else:
                self.icon_path = ""

        elif current_os == "Windows":
            # TODO: icon path loading for Windows
            logging.info("Icon path loading is not available for windows")
        else:
            raise Exception("OS name invalid or not found!")

    def print(self):
        """
        Prints the content of the app item
        """
        logging.info("************** App Item **************")
        logging.info("Label: {}".format(self.label))
        logging.info("App Path: {}".format(self.app_path))
        logging.info("App Bundle ID: {}".format(self.app_bundle_id))
        logging.info("Icon Path: {}".format(self.icon_path))
        logging.info("Softblock: {}".format(self.softblock))
        logging.info("Allow Interval: {}".format(self.allow_interval))
        if self.popup_item:
            logging.info("Popup Item ID:{}".format(self.popup_item.id))
        else:
            logging.info("Popup Item ID: None")


class LentoWebsiteItem(LentoBlockItem):
    """
    Class containing all information of a website item
    """

    def __init__(
        self, website_url, softblock=False, popup_item=None, allow_interval=60
    ):
        """
        Parameters:
        website_url: url of website to block
        softblock: whether the block item is softblocked
        popup_item: the popup item associated with the block item
        allow_interval: how long this block item will be allowed for
        """
        super().__init__(
            softblock=softblock, popup_item=popup_item, allow_interval=allow_interval
        )
        self.label = website_url
        self.website_url = website_url

    def save(self, parent_card):
        """
        Load the favicon associated with the url and save the website
        item to lento settings under a parent card item
        """
        self.icon_path = IconManager.load_favicon(self.website_url)
        CardsManagement.save_website_item(parent_card, self)

    def delete(self, parent_card):
        """
        Delete the website item from lento settings under a parent
        card item
        """
        CardsManagement.delete_website_item(parent_card, self)

    def print(self):
        """
        Prints the content of the website item
        """
        logging.info("************** Website Item **************")
        logging.info("Label: {}".format(self.label))
        logging.info("Website URL: {}".format(self.website_url))
        logging.info("Icon Path: {}".format(self.icon_path))
        logging.info("Softblock: {}".format(self.softblock))
        logging.info("Allow Interval: {}".format(self.allow_interval))
        if self.popup_item:
            logging.info("Popup Item ID:{}".format(self.popup_item.id))
        else:
            logging.info("Popup Item ID: None")


class LentoPopUpItem:
    """
    Class containing all information of a custom popup
    Also manages all popup item lifecycle
    """

    # list of objects that will be notified when a
    # popup item is deleted
    # all observer objects must implement
    # "onPopupDeleted(popup_id)" method
    popupDeletionObservers = []

    def __init__(self, id=None, msg=None):
        """
        Parameters:
        id: ID of the popup
        msg: custom message associated with the popup
        """
        self.id = id
        self.msg = msg

    def update_msg(self, msg):
        """
        Update the custom message of the popup item
        """
        self.msg = msg
        CardsManagement.update_popup(self)

    def delete(self):
        """
        Delete the popup item from lento settings and
        notify all oberver objects of the deletion
        """
        CardsManagement.delete_popup(self)
        # notify all observer objects of the popup item deletion
        for observer in LentoPopUpItem.popupDeletionObservers:
            observer.onPopupDeleted(self.id)

    def add_observer(observer):
        """
        Class method that adds a deletion observer object
        """
        logging.info("Adding observer {}".format(observer))
        LentoPopUpItem.popupDeletionObservers.append(observer)

    def remove_observer(observer):
        """
        Class method that removes a deletion observer object
        """
        logging.info("Removing observer {}".format(observer))
        LentoPopUpItem.popupDeletionObservers.remove(observer)

    def get_popup_items_list():
        """
        Class method that returns a list of LentoPopUpItem
        object read from lento settings
        """
        return CardsManagement.get_popup_items_list()


class LentoCardItem:
    """
    Class containing all information of a card item
    """

    def __init__(self, id=None, duration=0, name=None, end_time=None):
        """
        Parameters:
        id: ID of the card item, if no ID is provided, a ID will
            be generated
        duration: time interval set on the card
        name: name of the card
        end_time: timestamp for when the card item will terminate
        """
        self.id = id

        # generate a ID if none is provided
        if self.id is None:
            self.id = str(uuid.uuid4().hex)

        self.name = name
        self.duration = duration
        self.end_time = end_time
        self.block_items = {}
        self.activated = False
        self.saved = False
        # time remaining indicates the amount
        # of time that is left for the card,
        # this is used to setup already
        # activated card on app launch
        self.time_remaining = duration

        LentoPopUpItem.add_observer(self)

    def contains(self, block_item):
        """
        Checks if a block item already exists in the card
        """
        for label in self.block_items:
            if label == block_item.label:
                return True

        return False

    def isDone(self):
        """
        Checks if the card is completed
        """
        if self.end_time is None:
            return False

        return time.time() > self.end_time

    def activate(self):
        """
        Activates the card item and mark the card item as
        activated in lento settings
        """
        self.activated = True

        # if no end time exists for the card item, this
        # means that the card is first started, compute
        # the end time and set time remaining as the
        # duration of the timer
        if self.end_time is None:
            self.end_time = time.time() + self.duration
            self.time_remaining = self.duration
            self.save_metadata()
        else:
            # if an end time exists for the card item, this
            # means that the card is resumed, compute the
            # time remainig on the card
            self.time_remaining = self.end_time - time.time()

        # mark the card as activated in lento settings
        CardsManagement.activate_card(self)

    def deactivate(self):
        """
        Deactivates the card item and clears the currently
        activated card item in lento settings
        """
        self.activated = False
        self.end_time = None
        self.time_remaining = 0
        CardsManagement.deactivate_active_card()
        self.save_metadata()

    def add_block_item(self, item):
        """
        Add a block item to the card
        """
        if not self.saved:
            self.save_metadata()
        self.block_items[item.label] = item
        item.save(self)

    def update_block_item(self, label, item):
        """
        Updates a block item in card
        """
        item.label = label
        self.block_items[item.label] = item
        item.save(self)

    def remove_block_item(self, item):
        """
        Removes a block item from card
        """
        self.block_items.pop(item.label)
        item.delete(self)

    def save(self):
        """
        Save the entire card content to lento settings
        """
        self.save_metadata()

        for label in self.block_items:
            item = self.block_items[label]
            item.save(self)

    def save_metadata(self):
        """
        Save the card metadata to lento settings
        """
        if self.saved is False:
            self.saved = True
        CardsManagement.update_card_metadata(self)

    def delete(self):
        """
        Delete the card from lento settings
        """
        CardsManagement.delete_card(self)
        LentoPopUpItem.remove_observer(self)

    def onPopupDeleted(self, popup_id):
        """
        Method that handles when a popup ID is deleted
        """
        logging.info("Card {}: observe popup id {} deleted".format(self.id, popup_id))

        # search the block items in the card, if the block
        # item uses the popup ID, set popup item of the block
        # item to None. Note that we do not need to update
        # lento settings here since it is expected that the
        # caller of onPopupDeleted also modifies lento
        # settings accordingly
        for label in self.block_items:
            item = self.block_items[label]
            if item.popup_item is not None:
                if item.popup_item.id == popup_id:
                    logging.info("Removing popup item" " for {}".format(item.label))
                    item.popup_item = None

    def print(self):
        """
        Prints the content of the card item
        """
        logging.info("************** Card Item **************")
        logging.info("ID: {}".format(self.id))
        logging.info("Name: {}".format(self.name))
        logging.info("Duration: {}".format(self.duration))
        logging.info("End Time: {}".format(self.end_time))
        logging.info("Block Items:")
        for label in self.block_items:
            item = self.block_items.get(label)
            item.print()
        logging.info("****************************************")
