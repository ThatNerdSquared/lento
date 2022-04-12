from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QWidget
from lento.common import cards_management as CardsManagement


class Title(QWidget):
    def __init__(self, current_card, refresh_handler):
        super().__init__()

        self.CURRENT_CARD = current_card
        self.refresh = refresh_handler

        title_layout = QHBoxLayout()

        self.title = QLineEdit(self.CURRENT_CARD)
        self.title.returnPressed.connect(self.update_title)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("cardtitle")

        title_layout.addWidget(self.title)
        self.setLayout(title_layout)

    def update_title(self):
        user_input = self.title.text()
        CardsManagement.update_metadata(
            self.CURRENT_CARD,
            "name",
            user_input
        )
        self.refresh()
