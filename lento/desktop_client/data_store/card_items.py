import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from PySide6.QtGui import QIcon


class BlockItemType(Enum):
    WEBSITE = 1
    APP = 1


@dataclass(kw_only=True)
class _LentoBlockItem(ABC):
    """
    Base class for any block items
    """

    card_id: UUID
    blockitem_id: UUID
    item_label: str = field(init=False)
    enabled: bool = True
    restricted_access: bool = False
    associated_popup_id: UUID
    allow_interval: int = 0
    icon: QIcon

    @abstractmethod
    def save(self, parent_card):
        """Will be implemented by child class."""

    @abstractmethod
    def delete(self, parent_card):
        """Will be implemented by child class."""

    @abstractmethod
    def log_item_data(self):
        """Will be implemented by child class."""


@dataclass(kw_only=True)
class LentoWebsiteItem(_LentoBlockItem):
    """
    Class containing all information of a website item
    """

    website_url: str

    def __post_init__(self):
        self.item_label = self.website_url.split("://")[-1]

    def save(self, parent_card):
        pass
        # """
        # Load the favicon associated with the url and save the website
        # item to lento settings under a parent card item
        # """
        # self.icon_path = IconManager.load_favicon(self.website_url)
        # CardsManagement.save_website_item(parent_card, self)

    def delete(self, parent_card):
        pass
        # """
        # Delete the website item from lento settings under a parent
        # card item
        # """
        # CardsManagement.delete_website_item(parent_card, self)

    def log_item_data(self):
        popup_id_msg = self.associated_popup_id or "None"
        log_msgs = [
            "************** Website Item **************",
            f"Label: {self.item_label}",
            f"Website URL: {self.website_url}",
            f"Icon Path: {self.icon_path}",
            f"Softblock: {self.restricted_access}",
            f"Allow Interval: {self.allow_interval}",
            f"Popup Item ID: {popup_id_msg}",
        ]
        for msg in log_msgs:
            logging.info(msg)
