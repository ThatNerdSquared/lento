from typing import List
from uuid import UUID

from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtGui import QIcon

from lento.desktop_client.data_store import BackendType, datastore
from lento.desktop_client.data_store.card_items import LentoWebsiteItem


class WebsiteListModel(QAbstractListModel):
    def __init__(self, card_id: UUID):
        super().__init__()
        self.blocked_items: List[LentoWebsiteItem] = self._load_list_model(card_id)

    def _load_list_model(card_id):
        return datastore.get_website_list(card_id=card_id)[BackendType.JSON]

    def data(self, index, role):
        match role:
            case Qt.DisplayRole:
                return self.blocked_items[index].item_label
            case Qt.DecorationRole:
                return QIcon(self.blocked_items[index].icon_path)
            case Qt.TextAlignmentRole:
                return Qt.AlignHCenter

    def rowCount(self) -> int:
        return len(self.blocked_items)
