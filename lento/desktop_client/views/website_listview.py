from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QFrame, QListView, QSizePolicy

from lento.desktop_client.model.website_list_model import WebsiteListModel


class WebsiteListView(QListView):
    def __init__(self):
        super().__init__()
        websitelist_model = WebsiteListModel()
        self.setModel(websitelist_model)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.setFrameShape(QFrame.NoFrame)
        self.setShowGrid(False)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
