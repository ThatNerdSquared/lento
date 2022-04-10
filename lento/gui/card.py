from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QScrollArea  # noqa: E501
from lento.gui.hard_block_list import HBWebsitesList


class Card(QWidget):
    def __init__(self, DATA, refresh_handler):
        super().__init__()

        body_layout = QVBoxLayout()

        # Draw the card rect.
        body_rect = QFrame()
        body_rect.setFrameShape(QFrame.Panel)
        body_rect.setFrameShadow(QFrame.Raised)
        body_rect.setLineWidth(3)
        body_rect.setMidLineWidth(3)
        body_rect.setStyleSheet("QFrame { background-color: #FFFFFF; }")  # noqa: E501
        body_rect.setMinimumSize(300, 500)
        body_rect.setMaximumSize(500, 800)

        internal_card = QVBoxLayout()

        hb_list = HBWebsitesList(
            DATA["name"],
            DATA["hard_blocked_sites"],
            refresh_handler
        )
        internal_card.addWidget(hb_list)

        internal_card_widget = QWidget()
        internal_card_widget.setMinimumSize(250, 500)
        internal_card_widget.setMaximumSize(500, 800)
        internal_card_widget.setLayout(internal_card)

        # Set the internal scroll area for the card.
        scroll_area = QScrollArea()
        scroll_area.setWidget(internal_card_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_box = QVBoxLayout()
        scroll_box.addWidget(scroll_area)
        body_rect.setLayout(scroll_box)

        body_layout.addWidget(body_rect)
        self.setLayout(body_layout)
