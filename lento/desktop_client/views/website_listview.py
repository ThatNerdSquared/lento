from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QFrame, QListView, QSizePolicy

from lento.desktop_client.model.website_list_model import WebsiteListModel


class WebsiteListView(QListView):
    def __init__(self, card_id):
        super().__init__()
        websitelist_model = WebsiteListModel(card_id)
        self.setModel(websitelist_model)
        # HELLO, ME FROM THE FUTURE!!
        # I believe the last thing you were attempting to do
        # was to create a delegate to pop up the editing view
        # for website items.
        # self.setItemDelegate()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
