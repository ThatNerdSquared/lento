from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget  # noqa: E501
from lento.gui.timer import TimerView
from lento.gui.title import Title
from lento.gui.toggle_list import ToggleList


class Card(QWidget):
    def __init__(self, DATA, activated_card, refresh_handler):
        super().__init__()

        self.ACTIVATED_CARD = activated_card
        self.TIME = DATA["time"]

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

        title = Title(DATA["name"], refresh_handler)
        timer = TimerView(
            DATA["name"],
            self.TIME,
            self.ACTIVATED_CARD,
            refresh_handler
        )
        goal_list = ToggleList(
            DATA["name"],
            DATA["goals"],
            "goals",
            "    Goals",
            "GoalList",
            refresh_handler
        )
        whb_list = ToggleList(
            DATA["name"],
            DATA["hard_blocked_sites"],
            "hard_blocked_sites",
            "    Hard-blocked Websites",
            "WebsiteList",
            refresh_handler
        )
        wsb_list = ToggleList(
            DATA["name"],
            DATA["soft_blocked_sites"],
            "soft_blocked_sites",
            "    Soft-blocked Websites",
            "WebsiteList",
            refresh_handler
        )
        ahb_list = ToggleList(
            DATA["name"],
            DATA["hard_blocked_apps"],
            "hard_blocked_apps",
            "    Hard-blocked Apps",
            "AppList",
            refresh_handler
        )
        asb_list = ToggleList(
            DATA["name"],
            DATA["soft_blocked_apps"],
            "soft_blocked_apps",
            "    Soft-blocked Apps",
            "AppList",
            refresh_handler
        )

        internal_card.addWidget(title)
        internal_card.addWidget(timer)
        internal_card.addWidget(goal_list)
        internal_card.addWidget(whb_list)
        internal_card.addWidget(wsb_list)
        internal_card.addWidget(ahb_list)
        internal_card.addWidget(asb_list)

        internal_card_widget = QWidget()
        internal_card_widget.setObjectName("maincard")
        internal_card_widget.setLayout(internal_card)

        # Set the internal scroll area for the card.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(internal_card_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_box = QVBoxLayout()
        scroll_box.addWidget(scroll_area)
        body_rect.setLayout(scroll_box)

        body_layout.addWidget(body_rect)
        self.setLayout(body_layout)
