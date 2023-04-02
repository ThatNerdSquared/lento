import copy
import logging
import platform
from lento import utils
from PySide6.QtGui import QIcon, Qt, QPixmap
from PySide6.QtWidgets import QFileDialog, QSpinBox
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)  # noqa: E501
from lento.views.textedit import LentoTextEdit
from lento.viewcontrollers.popup_list import LentoPopUpList
from lento.model.block_items import LentoAppItem, LentoWebsiteItem
from lento.views.toggle import Toggle


class LentoBlockItemDetailsViewMode:
    """
    Defines the operating modes of the block item details view
    """

    APP = 0
    WEBSITE = 1


class LentoBlockItemDetailsView(QWidget):
    """
    Widget to display information of a block item or
    help to create a new block item
    """

    def __init__(self, block_item=None, mode=LentoBlockItemDetailsViewMode.WEBSITE):
        """
        Parameters:
        block_item: the block item to display, if None, display
            UI elements for block item creation
        mode: operating mode of the widget, if a block item is
            supplied, the operating mode will be ignored and
            will be based on the supplied block item
        """
        super().__init__()

        # determine the operating mode based on the supplied
        # block item
        if block_item is not None:
            if isinstance(block_item, LentoAppItem):
                self.mode = LentoBlockItemDetailsViewMode.APP
            elif isinstance(block_item, LentoWebsiteItem):
                self.mode = LentoBlockItemDetailsViewMode.WEBSITE
        # if no block item is supplied, use the operating
        # mode in the initializer
        else:
            self.mode = mode

        # build the widget layout
        self._build_layout()

        # deep copy the supplied block item; this is because
        # we may use a copy of the supplied block item as a
        # basis to build the modified block item after user
        # edit, but we do not want ot change the original
        # block item that is passed in
        if block_item is not None:
            self.block_item = copy.deepcopy(block_item)
        else:
            self.block_item = None

        # if a block item is supplied, setup the UI to
        # display block item information
        if block_item is not None:
            if self.mode == LentoBlockItemDetailsViewMode.APP:
                self._load_app_item(self.block_item)
                # hide the app edit button if an app item
                # is already supplied
                self.app_edit_button.setVisible(False)
            elif self.mode == LentoBlockItemDetailsViewMode.WEBSITE:
                self.web_text_edit.setText(block_item.website_url)
                # make the web url text box readonly if
                # a website item is already supplied
                self.web_text_edit.readonly = True
                self.web_text_edit.setAlignment(Qt.AlignCenter)

            if block_item.softblock:
                self.ra_toggle.setChecked(True)
                self.bi_spin.setValue(block_item.allow_interval / 60)

            if block_item.popup_item:
                # if the popup item is not found, this means the item is
                # previously deleted, remove the popup id from the item
                # in lento settings
                if not self.popup_list.selectPopup(block_item.popup_item.id):
                    logging.info(
                        "popup item with ID {} not found for {}".format(
                            block_item.popup_item.id, block_item.label
                        )
                    )
                    block_item.popup_item = None
                    block_item.save()

    def _build_layout(self):
        """
        Set up the base UI element layout of the window
        """
        body_layout = QVBoxLayout()

        # build the view for selecting app or website
        selection_widget = QWidget()
        selection_widget_layout = QVBoxLayout()
        selection_widget.setLayout(selection_widget_layout)
        selection_widget_layout.setContentsMargins(0, 0, 0, 0)

        # add error message first as hidden and make it
        # visible in case of error
        self.error_msg = QLabel()
        self.error_msg.setObjectName("add_window_error_msg")
        self.error_msg.setAlignment(Qt.AlignCenter)
        self.error_msg.setVisible(False)

        if self.mode == LentoBlockItemDetailsViewMode.APP:
            # build the widget for app selection
            self.app_add_button = QPushButton("Select an app...")
            self.app_add_button.setObjectName("add_window_add_btn")
            self.app_add_button.clicked.connect(self._on_add_app_clicked)

            self.app_widget = QWidget()
            app_widget_layout = QHBoxLayout()
            app_widget_layout.setContentsMargins(0, 0, 0, 0)
            self.app_widget.setLayout(app_widget_layout)
            self.app_widget.setObjectName("add_window_app_panel")
            self.app_widget.setVisible(False)

            self.app_icon = QPushButton()
            self.app_icon.setObjectName("add_window_app_icon")

            self.app_path_label = QLabel("")
            self.app_path_label.setWordWrap(True)
            self.app_path_label.setMinimumWidth(250)
            self.app_path_label.setObjectName("add_window_app_label")

            self.app_edit_button = QPushButton()
            self.app_edit_button.setIcon(
                QIcon(utils.get_data_file_path("assets/edit.svg"))
            )
            self.app_edit_button.clicked.connect(self._on_edit_app_clicked)
            self.app_edit_button.setObjectName("add_window_app_edit_button")
            edit_hover_path = utils.get_data_file_path("assets/edit_hover.svg")
            self.app_edit_button.setStyleSheet(
                "#add_window_app_edit_button:hover {{"
                "image: url({});"
                "}}".format(edit_hover_path)
            )

            app_widget_layout.addWidget(self.app_icon)
            app_widget_layout.addWidget(self.app_path_label)
            app_widget_layout.addStretch()
            app_widget_layout.addWidget(self.app_edit_button)

            self.error_msg.setText("No app selected")

            selection_widget_layout.addWidget(self.app_add_button)
            selection_widget_layout.addWidget(self.app_widget)

        elif self.mode == LentoBlockItemDetailsViewMode.WEBSITE:
            # build the widget for website url entry
            self.web_text_edit = LentoTextEdit(
                placeholder="Enter website URL to block..."
            )
            self.web_text_edit.setAlignment(Qt.AlignCenter)
            self.web_text_edit.setContentsMargins(0, 0, 0, 0)
            self.web_text_edit.textChangedHandler = self._on_website_entered
            self.web_check_msg = QLabel("Warning: This website URL maybe invalid")
            self.web_check_msg.setVisible(False)
            self.web_check_msg.setObjectName("add_window_web_chk_msg")

            self.error_msg.setText("No website entered")

            selection_widget_layout.addWidget(self.web_text_edit)
            selection_widget_layout.addWidget(self.web_check_msg)

        body_layout.addWidget(selection_widget)
        body_layout.addWidget(self.error_msg)

        # build restricted access toggle
        ra_widget = QWidget()
        ra_layout = QHBoxLayout()
        ra_layout.setContentsMargins(0, 0, 0, 0)
        ra_widget.setLayout(ra_layout)

        ra_text = QLabel("Restricted Access")
        ra_text.setObjectName("add_window_ra_text")
        ra_text.setContentsMargins(0, 0, 0, 0)
        tooltip_button = QPushButton()
        tooltip_button.setIcon(QIcon(utils.get_data_file_path("assets/help.svg")))
        tooltip_button.setObjectName("add_window_ra_icon")
        tooltip_button.setToolTip(
            "If Restricted Access is turned on, we will\n"
            "display popup and ask you if this item should\n"
            "be blocked every time we detect this item"
        )
        self.ra_toggle = Toggle()
        self.ra_toggle.onToggleStateChange = self._on_ra_toggled

        ra_layout.addWidget(ra_text)
        ra_layout.addWidget(tooltip_button)
        ra_layout.addStretch()
        ra_layout.addWidget(self.ra_toggle)
        body_layout.addWidget(ra_widget)

        # build the widget to enter allow interval
        # if restricted access toggle is on
        self.bi_widget = QWidget()
        bi_widget_layout = QHBoxLayout()
        bi_widget_layout.setContentsMargins(0, 0, 0, 20)
        self.bi_widget.setLayout(bi_widget_layout)
        self.bi_widget.setVisible(False)

        bi_label1 = QLabel("Remind me every ")
        bi_label1.setObjectName("add_window_bi_label")
        bi_label2 = QLabel("minutes")
        bi_label2.setObjectName("add_window_bi_label")
        self.bi_spin = QSpinBox()
        self.bi_spin.setRange(1, 180)
        self.bi_spin.setAlignment(Qt.AlignCenter)
        self.bi_spin.setValue(15)
        self.bi_spin.setObjectName("add_window_bi_spin")

        bi_widget_layout.addWidget(bi_label1)
        bi_widget_layout.addWidget(self.bi_spin)
        bi_widget_layout.addWidget(bi_label2)
        body_layout.addWidget(self.bi_widget)

        # setup the popup list
        popup_assign_text = QLabel("Assign a popup to this item...")
        popup_assign_text.setObjectName("add_window_popup_assign_text")
        body_layout.addWidget(popup_assign_text)

        self.popup_list = LentoPopUpList()

        body_layout.addWidget(self.popup_list)
        self.setLayout(body_layout)

    def get_block_item(self):
        """
        Returns:
        LentoAppItem or LentoWebsiteItem objects based
        on user input information in this widget
        """
        if self.mode == LentoBlockItemDetailsViewMode.APP:
            # if no block item exist it means no apps are
            # selected, return None
            if self.block_item is None:
                return None
        elif self.mode == LentoBlockItemDetailsViewMode.WEBSITE:
            selected_url = self.web_text_edit.toPlainText()
            # if no url is entered, return None
            if len(selected_url) == 0:
                return None

            # create a new website item based on the entered url
            self.block_item = LentoWebsiteItem(selected_url)

        # configure other properties of the block item
        if self.block_item:
            self.block_item.softblock = self.ra_toggle.handle_position == 1
            self.block_item.allow_interval = self.bi_spin.value() * 60
            self.block_item.popup_item = self.popup_list.selectedPopup()

        logging.info("Returning block item {}".format(self.block_item.label))
        return self.block_item

    def load_popups(self):
        """
        Reload the popup list
        """
        self.popup_list.updatePopups()

    def show_error_msg(self):
        """
        Make error message visible
        """
        self.error_msg.setVisible(True)

    def clear_error_msg(self):
        """
        Hide the error message
        """
        self.error_msg.setVisible(False)

    def _on_website_entered(self, text):
        """
        Method called when a website url is entered
        """
        # display an error message if website url is deleted
        if len(text) == 0:
            self.web_check_msg.setVisible(False)
            return

        # if url does not begin with https:// add it
        # TODO: this is hacky, what if the URL begins with http://?
        if text[:7] != "https://":
            text = "https://" + text

        # check if the entered url is of good format;
        # if not, display web url warning message
        if not utils.is_url(text):
            self.web_check_msg.setVisible(True)
        else:
            self.web_check_msg.setVisible(False)

        # clear the error message
        self.clear_error_msg()

    def _load_app_item(self, app_item):
        """
        Load the view according the supplied app item
        """
        # set the icon if it exists
        if app_item.icon_path:
            self.app_icon.setVisible(True)
            self.app_icon.setIcon(QIcon(QPixmap(app_item.icon_path)))
        else:
            self.app_icon.setVisible(False)

        self.app_path_label.setText(app_item.app_path)
        self.app_widget.setVisible(True)
        self.app_add_button.setVisible(False)

        # clear the error message
        self.clear_error_msg()

    def _on_add_app_clicked(self):
        """
        Handles when select app button is clicked
        """
        self._show_app_picker()

    def _on_edit_app_clicked(self):
        """
        Handles when edit app button is clicked
        """
        self._show_app_picker()

    def _on_ra_toggled(self, checked):
        """
        Handles when restricted access toggle is flipped
        """
        # when restricted access toggle is on,
        # display the view to configure access interval
        if checked:
            self.bi_widget.setVisible(True)
        else:
            self.bi_widget.setVisible(False)

    def _show_app_picker(self):
        """
        Display a window to pick apps
        """
        match platform.system():
            case "Darwin":
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.ExistingFiles)
                dialog.setDirectory("/Applications/")
                dialog.setNameFilter(("Applications (*.app)"))
                if dialog.exec():
                    app_path = dialog.selectedFiles()[0]
                    logging.info("Selecting app {}".format(app_path))
                    self.block_item = LentoAppItem(app_path)
                    self._load_app_item(self.block_item)
            case "Windows":
                print("ow")
            case _:
                raise Exception(f"Platform '{platform.system}' not found!")
