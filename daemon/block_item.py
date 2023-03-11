import logging
from datetime import datetime


class BlockItem:
    """
    Class that defines the basic property of a blocked
    item, shared between AppBlockItem and WebsiteBlockItem
    """

    def __init__(self, owner, soft_block=False):
        self.owner = owner
        self.is_soft_block = soft_block
        # last asked is initialized to the smallest
        # date possible so the first time an item
        # is blocked, popup is displayed to ask
        # if the item is allowed
        self.last_asked = datetime.min
        self.is_allowed = False
        self.allow_interval = 0
        self.popup_msg = ""

    def print(self):
        logging.info("Owner: {}".format(self.owner))
        logging.info("Soft Block?: {}".format(self.is_soft_block))
        logging.info("Last Asked: {}".format(self.last_asked))
        logging.info("Is Allowed: {}".format(self.is_allowed))
        logging.info("Allow Interval: {}s".format(self.allow_interval))
        logging.info("Popup Message: {}".format(self.popup_msg))


class AppBlockItem(BlockItem):
    """
    Class that defines an app to be blocked
    """

    def __init__(self, procname, owner, soft_block=False):
        super().__init__(owner, soft_block=soft_block)
        self.procname = procname

    def print(self):
        logging.info("*************App: {}*************".format(self.procname))
        super().print()


class WebsiteBlockItem(BlockItem):
    """
    Class that defines a website to be blocked
    """
    def __init__(self, website_url, owner, soft_block=False):
        super().__init__(owner, soft_block=soft_block)
        self.website_url = website_url

    def print(self):
        logging.info("*************Website: {}*************"
                     .format(self.website_url))
        super().print()


class NotificationItem:
    """
    Class that defines a repeated notification to be displayed
    """
    def __init__(self, name, title, message, interval, owner):
        self.name = name
        self.title = title
        self.message = message
        self.interval = interval
        self.owner = owner
