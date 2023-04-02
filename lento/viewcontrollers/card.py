import logging
import lento.model.block_items as BlockItem
import lento.model.cards_management as CardsManagement
from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from lento.views.timer import TimerView
from lento.views.title import LentoCardTitle
from lento.views.button import LentoOneTimeButton
from lento.viewcontrollers.block_item_window import LentoBlockItemWindow
from lento.views.toggle_list import LentoToggleList
from lento.viewcontrollers.popups import LentoPopUpWindow, LentoPopUpMode
from daemon_interface.daemon_interface import LentoDaemonInterface


class Card(QWidget):
    """
    Widget containing all information of a card
    """

    def __init__(self, card_item, start_handler, completion_handler):
        """
        Parameters:
        card_item: LentoCardItem object containing the data of a card
        start_handler: method to be called when card is activated
        completion_handler: method to be called when card is completed
        """
        super().__init__()

        self.card_item = card_item
        self.start_handler = start_handler
        self.completion_handler = completion_handler
        self.daemon_interface = LentoDaemonInterface(logging.getLogger())

        # set drop shadow effect
        self.drop_shadow = QGraphicsDropShadowEffect(self)
        self.drop_shadow.setBlurRadius(20)
        self.drop_shadow.setOffset(0)
        self.drop_shadow.setYOffset(4)
        self.drop_shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.drop_shadow)

        body_rect = QWidget()
        body_rect.setObjectName("outercard")
        self.body_layout = QVBoxLayout()
        internal_card = QVBoxLayout()

        # setup title
        self.title = LentoCardTitle(self.card_item.name, self._on_title_updated)

        # setup timer box
        timer_box = QWidget()
        timer_box_layout = QVBoxLayout()
        timer_box_layout.setContentsMargins(10, 10, 10, 10)
        timer_box.setLayout(timer_box_layout)
        timer_box.setObjectName("widgetbox")
        timer_box.setAttribute(Qt.WA_StyledBackground, True)

        # setup timer
        self.timer = TimerView(
            card_item.duration, self._on_time_changed, self._on_timer_complete
        )

        # setup start button
        self.start_button = LentoOneTimeButton(
            "Start Block", "Running", self.on_start_button_clicked
        )

        # group timer & start button into one timer box widget
        timer_box_layout.addWidget(self.timer)
        timer_box_layout.addWidget(self.start_button)

        # setup the three toggle lists
        # toggle lists will be hidden when they do not
        # contain any block items
        self.list_widget = QWidget()
        list_widget_layout = QVBoxLayout()
        list_widget_layout.setContentsMargins(0, 0, 0, 0)
        list_widget_layout.setSpacing(0)
        self.list_widget.setLayout(list_widget_layout)

        self.web_list = LentoToggleList(
            "Websites",
            item_edited_handler=self._on_block_item_edit,
            item_removed_handler=self._on_block_item_remove,
        )
        self.web_list.setVisible(False)

        self.app_list = LentoToggleList(
            "Apps",
            item_edited_handler=self._on_block_item_edit,
            item_removed_handler=self._on_block_item_remove,
        )
        self.app_list.setVisible(False)

        self.ra_list = LentoToggleList(
            "Restricted Access",
            item_edited_handler=self._on_block_item_edit,
            item_removed_handler=self._on_block_item_remove,
        )
        self.ra_list.setVisible(False)

        list_widget_layout.addWidget(self.web_list)
        list_widget_layout.addWidget(self.app_list)
        list_widget_layout.addWidget(self.ra_list)

        # setup add app or website button
        self.add_app_web_button = QPushButton("+ Add an app or website")
        self.add_app_web_button.clicked.connect(self.on_add_button_clicked)
        self.add_app_web_button.setObjectName("appweb")

        internal_card.addWidget(self.title)
        internal_card.addWidget(timer_box)
        internal_card.addWidget(self.list_widget)
        internal_card.addWidget(self.add_app_web_button)

        internal_card_widget = QWidget()
        internal_card_widget.setObjectName("maincard")
        internal_card_widget.setLayout(internal_card)

        # Set the internal scroll area for the card
        scroll_area = QScrollArea()
        scroll_area.setAutoFillBackground(True)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(internal_card_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_box = QVBoxLayout()
        scroll_box.addWidget(scroll_area)
        body_rect.setLayout(scroll_box)

        self.body_layout.addWidget(body_rect)
        self.setLayout(self.body_layout)

        # record the initial height of the card, this will
        # help us resize the card as we add more block items
        self.initial_height = self.sizeHint().height()

        # load all block items stored in LentoCardItem object
        for label in self.card_item.block_items:
            block_item = self.card_item.block_items.get(label)
            self._show_block_item(block_item)

    def activate(self):
        """
        Configures UI elements in activated mode
        """
        logging.info("Activating card {}...".format(self.card_item.id))
        self.start_button.activate()
        self.card_item.activate()
        if self.card_item.duration != self.card_item.time_remaining:
            self.timer.set_time(self.card_item.time_remaining)
        self.timer.start()
        self.add_app_web_button.setEnabled(False)
        self.title.setEnabled(False)
        self.web_list.disable()
        self.app_list.disable()
        self.ra_list.disable()
        self.drop_shadow.setColor(QColor(200, 0, 0, 200))
        self.start_handler(self)

    def deactivate(self):
        """
        Configures UI elemets in deactivated mode
        """
        logging.info("Deactivating card {}...".format(self.card_item.id))
        self.card_item.deactivate()
        self.timer.reset()
        self.add_app_web_button.setEnabled(True)
        self.title.setEnabled(True)
        self.web_list.enable()
        self.app_list.enable()
        self.ra_list.enable()
        self.drop_shadow.setColor(QColor(0, 0, 0, 100))
        self.start_button.reset()

    def delete(self):
        """
        Delete the card
        """
        logging.info("Deleting card {}...".format(self.card_item.id))
        self.deactivate()
        self.card_item.delete()
        logging.info("Deleted card {}...".format(self.card_item.id))

    def on_add_button_clicked(self):
        """
        Handles when add button is clicked
        """
        logging.info("Showing new block item window")
        # show new LentoBlockItemWindow
        new_item_window = LentoBlockItemWindow(item_changed_handler=self._add_new_item)
        new_item_window.exec()

    def on_start_button_clicked(self):
        """
        Handles when start button is clicked
        """

        logging.info("Start Button for card {} clicked".format(self.card_item.id))

        # cannot satrt block if there are no block items
        if len(self.card_item.block_items) == 0:
            logging.info("card {} has 0 block items".format(self.card_item.id))
            LentoPopUpWindow(
                "No items to block, card cannot be started", mode=LentoPopUpMode.ERROR
            ).exec()
            return

        # cannot start block if block duration is 0
        if self.card_item.duration == 0:
            logging.info("card {} has 0 duration".format(self.card_item.id))
            LentoPopUpWindow(
                "Zero card duration, card cannot be started", mode=LentoPopUpMode.ERROR
            ).exec()
            return

        card_dict = CardsManagement.get_card_dict(self.card_item)

        # cannot start block if failed to fetch card dictionary
        if card_dict is None:
            logging.info(
                "Failed to fetch card dict with id {}".format(self.card_item.id)
            )
            LentoPopUpWindow("Failed to start block", mode=LentoPopUpMode.ERROR).exec()
            return

        duration = card_dict.get("duration")
        duration = float(duration)

        logging.info(
            "Starting block with dictionary: {}; duration: {}".format(
                card_dict, duration
            )
        )

        try:
            # launch card task in daemon
            ret = self.daemon_interface.start_block_timer(
                card_dict, duration, launch_daemon=True
            )
        except Exception:
            ret = False

        if ret is False:
            logging.info(
                "Failed to launch block task for card {}".format(self.card_item.id)
            )
            LentoPopUpWindow("Failed to start block", mode=LentoPopUpMode.ERROR).exec()
            return

        self.activate()

    def adjust_height(self):
        """
        Adjusts the height of the card according to the items
        in the toggle lists
        """
        new_height = (
            self.initial_height
            + self.web_list.list_height(self)
            + self.app_list.list_height(self)
            + self.ra_list.list_height(self)
            + self.add_app_web_button.height()
        )
        self.setFixedHeight(new_height)

    def _add_new_item(self, block_item):
        """
        Method called when a new block item is added,
        adds the block item to card view and the card item

        Returns:
        True if the block item is successfully added
        False otherwise
        """
        if not self.card_item.contains(block_item):
            logging.info("Adding new block item {}".format(block_item.label))
            self.card_item.add_block_item(block_item)
            self._show_block_item(block_item)
            return True

        LentoPopUpWindow(
            "Block item {} cannot be added because it is"
            " already in card".format(block_item.label),
            mode=LentoPopUpMode.ERROR,
        ).exec()

        return False

    def _show_block_item(self, block_item):
        """
        Displays a block item in the corresponding toggle list
        """

        # find the corresponding list for the block item
        list_widget = None
        if block_item.softblock:
            list_widget = self.ra_list
        elif isinstance(block_item, BlockItem.LentoWebsiteItem):
            list_widget = self.web_list
        elif isinstance(block_item, BlockItem.LentoAppItem):
            list_widget = self.app_list

        if list_widget:
            # make the list visible if this is the first
            # block item added to the list
            if list_widget.count() == 0:
                list_widget.setVisible(True)

            list_widget.add_to_list(block_item)
            # adjust height of the card after adding the element
            self.adjust_height()

    def _on_block_item_edit(self, toggle_list, old_block_item, new_block_item):
        """
        Method called when a block item is edited in a toggle list
        """
        logging.info(
            "{} block item edited; old soft block = {};"
            " new soft block = {}".format(
                old_block_item.label, old_block_item.softblock, new_block_item.softblock
            )
        )

        # the softblock property of the edited item may differ from the
        # softblock property of the original item; if this is the case,
        # we need to remove the original item from its corresponding
        # toggle list and add the new item in its corresponding toggle
        # list (example: moving from restricted access list to hard block
        # list if restricted access is disabled after edit)
        if old_block_item.softblock != new_block_item.softblock:
            # remove the block item from the toggle list, this will invoke
            # _on_block_item_remove callback which will also remove the
            # block item from the card item
            toggle_list.remove_from_list(old_block_item)
            # add the new item back into the card, under the corresponding
            # toggle list
            self._add_new_item(new_block_item)

        # update the block item label in the card item
        self.card_item.update_block_item(old_block_item.label, new_block_item)

    def _on_block_item_remove(self, toggle_list, block_item):
        """
        Method called when a block item is removed from a toggle list
        """

        logging.info(
            "Removing block item {} from card {}".format(
                block_item.label, self.card_item.id
            )
        )

        # make the list invisible if it no longer contains
        # any block item
        if toggle_list.count() == 0:
            toggle_list.setVisible(False)

        # remove the block item from card item
        self.card_item.remove_block_item(block_item)

    def _on_title_updated(self, title):
        """
        Method called when the title is updated
        """

        # check if the card title already exists;
        # if it does, display error popup and reset the
        # title to the original card title
        card_name_set = CardsManagement.get_all_card_names()
        if title != self.card_item.name and title in card_name_set:
            self.title.title.setText(self.card_item.name)
            LentoPopUpWindow(
                "Card name {} already exists".format(title), mode=LentoPopUpMode.ERROR
            ).exec()
            return

        logging.info("Changing card {} title to {}".format(self.card_item.id, title))
        self.card_item.name = title
        self.card_item.save_metadata()

    def _on_time_changed(self, new_duration):
        """
        Method called when timer time is changed
        """

        # if the time is changed to 0, reset the timer
        # time back to the original duration
        if new_duration == 0:
            self.timer.set_time(self.card_item.duration)
            LentoPopUpWindow(
                "Card duration cannot be 0", mode=LentoPopUpMode.ERROR
            ).exec()
            return

        logging.info(
            "Changing card {} duration to {}".format(self.card_item.id, new_duration)
        )
        self.card_item.duration = new_duration
        self.card_item.save_metadata()

    def _on_timer_complete(self):
        """
        Method called when timer is complete
        """

        # reset the card and call completion handler
        self.deactivate()
        self.completion_handler(self)
