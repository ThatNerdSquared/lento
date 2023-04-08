from typing import List
from uuid import UUID

from PySide6.QtCore import QAbstractListModel, Qt

from lento.desktop_client.data_store import BackendType, datastore
from lento.desktop_client.data_store.card_items import LentoWebsiteItem


class WebsiteListModel(QAbstractListModel):
    def __init__(self, card_id: UUID):
        super().__init__()
        self.blocked_items: List[LentoWebsiteItem] = self._load_list_model(card_id)

    def _load_list_model(self, card_id):
        return datastore.get_website_list(card_id=card_id)[BackendType.JSON]

    def data(self, index, role):
        item = self.blocked_items[index.row()]
        match role:
            case Qt.DisplayRole:
                return item.item_label
            case Qt.DecorationRole:
                return item.icon
            case Qt.TextAlignmentRole:
                return Qt.AlignLeft

    def rowCount(self, index=None) -> int:
        return len(self.blocked_items)
