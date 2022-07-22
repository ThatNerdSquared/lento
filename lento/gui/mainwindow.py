import sys
from lento.common.init_sequence import init_sequence
from lento.gui.card import Card
from lento import utils
from pathlib import Path
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QToolButton, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget  # noqa: E501
from lento.common import cards_management as CardsManagement
# from lento.gui.notifications import NotifWindow
from lento.common.cards_management import create_card


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lento")

        self.set_up_window()

    def set_up_window(self):
        main = QWidget()
        self.deck = QStackedWidget()

        main_layout = QHBoxLayout()
        main.setLayout(main_layout)
        main.setObjectName("mainwindow")

        notif_window = QWidget()
        self.SYSTEMS_WIDGETS = {
            "notif_window": notif_window
        }

        for item in self.SYSTEMS_WIDGETS.keys():
            self.deck.addWidget(self.SYSTEMS_WIDGETS[item])

        left_button = QToolButton()
        left_button.setIcon(QIcon(
            utils.get_data_file_path("assets/arrow-left.svg")
        ))
        left_button.setIconSize(QSize(70, 70))
        left_button.setObjectName("emojibutton")
        left_button.clicked.connect(self.left_button_click)
        main_layout.addWidget(left_button)

        cards = CardsManagement.read_cards()
        ACTIVATED_CARD = CardsManagement.get_block_in_settings()

        if len(cards) == 0:
            create_card(0)

        for item in cards.keys():
            card_buttons = QWidget()
            card_buttons_layout = QVBoxLayout()

            menu_buttons = QWidget()
            menu_buttons_layout = QHBoxLayout()

            add_card = QToolButton()
            add_card.setIcon(QIcon(
                utils.get_data_file_path("assets/add-twemoji.svg")
            ))
            add_card.setIconSize(QSize(30, 30))
            add_card.setObjectName("emojibutton")

            delete_card = QToolButton()
            delete_card.setIcon(QIcon(
                utils.get_data_file_path("assets/delete-twemoji.svg")
            ))
            delete_card.setIconSize(QSize(30, 30))
            delete_card.setObjectName("emojibutton")

            menu_buttons_layout.addWidget(add_card)
            menu_buttons_layout.addWidget(delete_card)
            menu_buttons.setLayout(menu_buttons_layout)

            _card = Card(cards[item], ACTIVATED_CARD, self.refresh_event)

            card_buttons_layout.addWidget(_card)
            card_buttons_layout.addWidget(menu_buttons)
            card_buttons.setLayout(card_buttons_layout)

            self.deck.addWidget(card_buttons)

        main_layout.addWidget(self.deck)

        right_button = QToolButton()
        right_button.setIcon(QIcon(
            utils.get_data_file_path("assets/arrow-right.svg")
        ))
        right_button.setIconSize(QSize(70, 70))
        right_button.setObjectName("emojibutton")
        right_button.clicked.connect(self.right_button_click)
        main_layout.addWidget(right_button)

        self.deck.setCurrentIndex(len(self.SYSTEMS_WIDGETS))

        self.setCentralWidget(main)

    def left_button_click(self):
        sys_windows = len(self.SYSTEMS_WIDGETS)
        deck_len = self.deck.count()
        index = self.deck.currentIndex()

        if index != 0:
            index -= 1
            self.deck.setCurrentIndex(index)
        else:
            self.deck.setCurrentIndex(index + deck_len - 1 - sys_windows)

        print(index, "left")

    def right_button_click(self):
        sys_windows = len(self.SYSTEMS_WIDGETS)
        deck_len = self.deck.count()
        index = self.deck.currentIndex()

        if index + 1 + sys_windows != deck_len:
            index += 1
            self.deck.setCurrentIndex(index)
        else:
            self.deck.setCurrentIndex(0)

        print(index, "right")

    def flipper(self):
        self.deck.setCurrentIndex(0)

    def refresh_event(self):
        self.set_up_window()


def main():
    app = QApplication(sys.argv)

    fonts = utils.get_data_file_path('fonts')
    for font in QDir(fonts).entryInfoList("*.ttf"):
        QFontDatabase.addApplicationFont(font.absoluteFilePath())
    stylesheet_path = Path(utils.get_data_file_path("lento.qss"))
    app.setStyleSheet(stylesheet_path.read_text())

    init_sequence()

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
