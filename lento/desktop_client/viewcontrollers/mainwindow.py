import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

import lento.desktop_client.data_store.datastore as datastore
import lento.desktop_client.data_store.icon_manager as IM
from lento.config import Config
from lento.desktop_client import utils
from lento.desktop_client.data_store.json_data_backend import JSONDataBackend
from lento.desktop_client.model import cards_management as CardsManagement
from lento.desktop_client.model.block_items import LentoCardItem
from lento.desktop_client.viewcontrollers.card import Card
from lento.desktop_client.viewcontrollers.popups import LentoPopUpMode, LentoPopUpWindow


class MainWindow(QMainWindow):
    """
    Main App Window
    Manages the deck of cards and card life cycle
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lento")
        self._set_up_window()

    def _set_up_window(self):
        """
        Setup main window views
        """

        main = QWidget()
        self.deck = QStackedWidget()
        self.main_layout = QHBoxLayout()

        # set left button
        self.left_button = QToolButton()
        self.left_button.setIcon(
            QIcon(utils.get_data_file_path("assets/arrow-left.svg"))
        )
        self.left_button.setIconSize(QSize(70, 70))
        self.left_button.setObjectName("emojibutton")
        self.left_button.clicked.connect(self.left_button_click)

        # set right button
        self.right_button = QToolButton()
        self.right_button.setIcon(
            QIcon(utils.get_data_file_path("assets/arrow-right.svg"))
        )
        self.right_button.setIconSize(QSize(70, 70))
        self.right_button.setObjectName("emojibutton")
        self.right_button.clicked.connect(self.right_button_click)

        # load current cards from lentosettings
        cards = CardsManagement.read_cards()
        logging.info("{} cards loaded from config: {}".format(len(cards), cards.keys()))

        # clean up unused icons saved in application support directory
        IM.cleanup_saved_icon(cards)

        # load activated card
        card_to_activate = None
        activated_card_id = CardsManagement.get_activated_card_id()
        logging.info("Loaded activated card id: {}".format(activated_card_id))

        if activated_card_id is not None:
            card_item = cards.get(activated_card_id)
            if card_item is not None:
                # if the activated card item is already done, deactivated it
                if card_item.isDone():
                    logging.info(
                        "Card {} ended at {}, deactivating...".format(
                            activated_card_id, card_item.end_time
                        )
                    )
                    card_item.deactivate()
                    activated_card_id = None

            else:
                # if the activated card does not exist in lento settings,
                # remove the activated card id from lento settings
                logging.info(
                    "Card id {} does not exist in cards dict,"
                    " deactivating...".format(activated_card_id)
                )
                CardsManagement.deactivate_active_card()

        # create a card for each card item loaded
        for card_id in cards:
            card_item = cards[card_id]
            logging.info("Loading card id {}".format(card_id))
            card_item.print()
            card = Card(card_item, self.on_card_started, self.on_card_complete)

            # save the currently active card and
            # activate the card after all view
            # elements are set up
            if card_item.id == activated_card_id:
                card_to_activate = card

            self.deck.addWidget(card)

        # if there are no cards in lentosettings, create
        # empty card
        if len(cards) == 0:
            logging.info("No existing card, adding empty new card...")
            self.add_card()
        else:
            self.deck.setCurrentIndex(0)

        # build menu bar at the bottom
        self.add_card_button = QToolButton()
        self.add_card_button.setIcon(
            QIcon(utils.get_data_file_path("assets/add-twemoji.svg"))
        )
        self.add_card_button.setIconSize(QSize(30, 30))
        self.add_card_button.setObjectName("emojibutton")
        self.add_card_button.clicked.connect(self.add_card)

        self.trash_card_button = QToolButton()
        self.trash_card_button.setIcon(
            QIcon(utils.get_data_file_path("assets/delete-twemoji.svg"))
        )
        self.trash_card_button.setIconSize(QSize(30, 30))
        self.trash_card_button.setObjectName("emojibutton")
        self.trash_card_button.clicked.connect(self.trash_current_card)

        menu_buttons = QWidget()
        menu_buttons_layout = QHBoxLayout()

        menu_buttons_layout.addWidget(self.add_card_button)
        menu_buttons_layout.addWidget(self.trash_card_button)
        menu_buttons.setLayout(menu_buttons_layout)

        # setup layout for card & bottom deck
        deck_domain = QWidget()
        deck_domain_layout = QVBoxLayout()
        deck_domain_layout.addWidget(self.deck)
        deck_domain_layout.addWidget(menu_buttons)
        deck_domain.setLayout(deck_domain_layout)

        # setup main window layout
        self.main_layout.addWidget(self.left_button)
        self.main_layout.addWidget(deck_domain)
        self.main_layout.addWidget(self.right_button)
        main.setLayout(self.main_layout)
        main.setObjectName("mainwindow")
        self.setCentralWidget(main)

        # activate the currently active card
        if card_to_activate is not None:
            logging.info("Activating card {}...".format(card_to_activate.card_item.id))
            card_to_activate.activate()

    def left_button_click(self):
        """
        Handles left button click
        """

        index = self.deck.currentIndex()
        deck_len = self.deck.count()
        card = self.deck.currentWidget()

        if deck_len == 1:
            return

        # if the current card is not saved, display warning popup
        # warning that the current unsaved card will be deleted
        if not card.card_item.saved:
            logging.info("Current card is not saved, showing warning popup...")
            ret = LentoPopUpWindow(
                "Current new card is unedited and will be deleted, " "OK to continue?",
                mode=LentoPopUpMode.WARNING,
            ).exec()

            if ret == 0:
                return
            else:
                # remove the unsaved card from the deck
                self.deck.removeWidget(card)
                card.setParent(None)
                deck_len -= 1
                index += 1

        if index - 1 >= 0:
            index -= 1
            self.deck.setCurrentIndex(index)
        else:
            # if the index is out of bounds, wrap around
            # to the last card in deck
            self.deck.setCurrentIndex(deck_len - 1)

    def right_button_click(self):
        """
        Handles right button click
        """

        deck_len = self.deck.count()
        index = self.deck.currentIndex()
        card = self.deck.currentWidget()

        if deck_len == 1:
            return

        # if the current card is not saved, display warning popup
        # warning that the current unsaved card will be deleted
        if not card.card_item.saved:
            logging.info("Current card is not saved, showing warning popup...")
            ret = LentoPopUpWindow(
                "Current new card is unedited and will be deleted, " "OK to continue?",
                mode=LentoPopUpMode.WARNING,
            ).exec()

            if ret == 0:
                return
            else:
                # remove the unsaved card from the deck
                self.deck.removeWidget(card)
                card.setParent(None)
                deck_len -= 1
                index -= 1

        if index + 1 < deck_len:
            index += 1
            self.deck.setCurrentIndex(index)
        else:
            # if the index is out of bounds, wrap around
            # to the first card in deck
            self.deck.setCurrentIndex(0)

    def add_card(self):
        """
        Handles add card button, adds a new card to deck
        """

        # new card has "New Card X" name by default,
        # find an index that is currently not used
        new_card_idx = 0
        new_card_name = "New Card"
        for i in range(self.deck.count()):
            widget = self.deck.widget(i)
            card_item = widget.card_item
            if card_item.name.startswith(new_card_name):
                new_card_idx += 1

        if new_card_idx != 0:
            new_card_name = new_card_name + " " + str(new_card_idx)

        # create the new card item
        new_card_item = LentoCardItem(name=new_card_name)
        new_card = Card(new_card_item, self.on_card_started, self.on_card_complete)

        # set the current card to the newly created card
        self.deck.addWidget(new_card)
        idx = self.deck.count() - 1
        self.deck.setCurrentIndex(idx)

    def trash_current_card(self):
        """
        Handles delete card button, deletes a card from deck
        """

        card = self.deck.currentWidget()

        # cannot delete a card that is currently activated and running
        if card.card_item.activated:
            logging.info(
                "Current card {} is running, skip deletion".format(card.card_item.id)
            )
            return

        # show popup confirming deletion
        ret = LentoPopUpWindow(
            "Are you sure you want to delete the current card?",
            mode=LentoPopUpMode.WARNING,
        ).exec()

        if ret == 0:
            return

        # delete the card from deck and lento settings
        logging.info("Deleting current card with id {}".format(card.card_item.id))
        if card.card_item.saved:
            card.delete()

        self.deck.removeWidget(card)
        card.setParent(None)

        # if there are no cards in deck after deletion,
        # add a new card
        if self.deck.count() == 0:
            logging.info("Card deck empty, creating empty card")
            self.add_card()

    def on_card_started(self, cardview):
        """
        Method called when a card is activated
        """

        logging.info("Card {} is activated".format(cardview.card_item.id))

        # disable all control buttons
        self.add_card_button.setEnabled(False)
        self.trash_card_button.setEnabled(False)
        self.right_button.setEnabled(False)
        self.left_button.setEnabled(False)

    def on_card_complete(self, cardview):
        """
        Method called when a card is completed
        """

        logging.info("Card {} completed".format(cardview.card_item.id))

        # enable all control buttons
        self.add_card_button.setEnabled(True)
        self.trash_card_button.setEnabled(True)
        self.right_button.setEnabled(True)
        self.left_button.setEnabled(True)


def init_sequence():
    """
    Initialization tasks before launching app
    """

    init_needed = False

    # setup logging: set up two logging handlers to log
    # both to file (RotatingFileHandler) and to console
    # (StreamHandler)
    log_file_path = Config.APPDATA_PATH / "lentogui.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - pid:%(process)d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RotatingFileHandler(
                log_file_path,
                mode="a",
                maxBytes=5 * 1024 * 1024,
                backupCount=2,
                encoding=None,
                delay=0,
            ),
            logging.StreamHandler(),
        ],
    )

    datastore.init_datastore(backends=[JSONDataBackend()])

    # Check for the lentosettings.json file, create if nonexistent
    try:
        Config.SETTINGS_PATH.read_text()
    except FileNotFoundError:
        logging.info("Creating blank config at {}".format(Config.SETTINGS_PATH))
        blank_config = {
            "activated_card": None,
            "cards": {},
            "application_settings": {"theme": "automatic"},
        }
        Config.SETTINGS_PATH.write_text(json.dumps(blank_config))
        init_needed = True

    # Create the correct application data folder for the platform,
    # unless it exists already.
    try:
        logging.info("Creating {}".format(Config.APPDATA_PATH))
        Config.APPDATA_PATH.mkdir(parents=True)
        init_needed = True
    except FileExistsError:
        logging.info("{} already exist".format(Config.APPDATA_PATH))

    try:
        logging.info("Creating {}".format(Config.ICON_PATH))
        Config.ICON_PATH.mkdir(parents=True)
        init_needed = True
    except FileExistsError:
        logging.info("{} already exist".format(Config.APPDATA_PATH))

    return init_needed


def main():
    app = QApplication(sys.argv)

    # load font asset
    fonts = utils.get_data_file_path("fonts")
    for font in QDir(fonts).entryInfoList("*.ttf"):
        QFontDatabase.addApplicationFont(font.absoluteFilePath())
    stylesheet_path = Path(utils.get_data_file_path("lento.qss"))
    app.setStyleSheet(stylesheet_path.read_text())

    # initialize lentosettings.json file and
    # create application data folder
    init_sequence()

    logging.info("Launching app...")

    # show main window
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
