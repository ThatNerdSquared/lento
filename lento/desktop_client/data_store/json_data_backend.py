import json
from typing import List
from uuid import UUID

from lento.config import Config

from . import BackendType
from ._abstract_data_backend import AbstractDataBackend
from .card_items import BlockItemType, LentoWebsiteItem
from .icon_manager import IconManager


class JSONDataBackend(AbstractDataBackend):
    def __init__(self):
        super().__init__()
        self.icon_manager = IconManager()

    def get_backend_type(self):
        return BackendType.JSON

    def get_website_list(self, card_id: UUID) -> List[LentoWebsiteItem]:
        raw_card_data = json.loads(Config.SETTINGS_PATH.read_text())
        websites_dict = raw_card_data["cards"][card_id]["blocked_sites"]
        res = []
        for site_id in websites_dict.keys():
            item = websites_dict[site_id]
            blockitem = LentoWebsiteItem(
                card_id=card_id,
                blockitem_id=site_id,
                enabled=item["enabled"],
                restricted_access=item["restricted_access"],
                associated_popup_id=item["associated_popup_id"],
                allow_interval=item["allow_interval"],
                icon=self.icon_manager.load_icon(
                    site_id, item["website_url"], BlockItemType.WEBSITE
                ),
                website_url=item["website_url"],
            )
            res.append(blockitem)
        return res
