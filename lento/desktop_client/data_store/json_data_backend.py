import json
from uuid import UUID

from _abstract_data_backend import AbstractDataBackend
from data_store import BackendType

from lento.config import Config


class JSONDataBackend(AbstractDataBackend):
    def __init__(self):
        super().__init__()

    def get_backend_type(self):
        return BackendType.JSON

    def get_website_list(card_id: UUID):
        raw_card_data = json.loads(Config.SETTINGS_PATH.read_text())
        websites_dict = raw_card_data["cards"][card_id]["blocked_sites"]
        res = []
        for site in websites_dict.keys():
            item = websites_dict[site]
            res.append(item)
        return res
