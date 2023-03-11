import logging
from PySide6 import QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame, QScrollArea, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton  # noqa: E501
from PySide6.QtCore import Qt
from lento.views.resizing_tab import ResizingTabWidget
from lento.viewcontrollers.block_item_details import LentoBlockItemDetailsView, LentoBlockItemDetailsViewMode # noqa: E501


class LentoBlockItemWindow(QDialog):
    """
    Window to display information for a block item or to create new block item
    """

    def __init__(self, block_item=None, item_changed_handler=None):
        """
        Parameters:
        block_item: the block item to display, if None, display
            UI elements for block item creation
        item_changed_handler: called when the changes are confirmed
            by the user, if item_changed_handler returns False,
            LentoBlockItemWindow will not be dismissed
        """
        super().__init__()

        self.tab = None
        self.item_view = None
        self.item_changed_handler = item_changed_handler

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        body_rect = QWidget()
        body_rect.setObjectName("outercard")
        body_layout = QVBoxLayout()

        # build control bar and control button 
        # located at the top of the window
        controlbar = QWidget()
        controlbar_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("add_window_cancel_btn")
        cancel_button.clicked.connect(self.on_cancel_clicked)
        confirm_button = QPushButton("Done")
        confirm_button.setObjectName("add_window_confirm_btn")
        confirm_button.clicked.connect(self.on_confirm_clicked)

        controlbar_layout.addWidget(cancel_button)
        controlbar_layout.addStretch()
        controlbar_layout.addWidget(confirm_button)
        controlbar.setLayout(controlbar_layout)

        internal_card = QVBoxLayout()
        internal_card_widget = QWidget()
        internal_card_widget.setObjectName("maincard")

        # if block item is supplied, use block item label
        # as title, otherwise use default title
        title = QLabel("Add New Block Item")
        if block_item is not None:
            title.setText(block_item.label)
        title.setMaximumWidth(400)
            
        title.setObjectName("itemtitle")
        internal_card.addWidget(title)
        title.setAlignment(Qt.AlignCenter)

        # if no block item is supplied, assume the window is
        # for adding new block item, create the tabs for 
        # different types of block items
        if block_item is None:
            self.tab = ResizingTabWidget()
            self.tab.addTab(LentoBlockItemDetailsView(mode=LentoBlockItemDetailsViewMode.APP), 'Apps')
            self.tab.addTab(LentoBlockItemDetailsView(mode=LentoBlockItemDetailsViewMode.WEBSITE), 'Website')
            self.tab.currentChanged.connect(self.on_tab_changed)
            internal_card.addWidget(self.tab)
        
        # if block item is supplied, only show info of 
        # provided block item
        else:
            self.item_view = LentoBlockItemDetailsView(block_item=block_item)
            internal_card.addWidget(self.item_view)

        # Set the internal scroll area for the card, add widgets to main layout
        internal_card_widget.setLayout(internal_card)
        scroll_area = QScrollArea()
        scroll_area.setAutoFillBackground(True)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(internal_card_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scrollbox_layout = QVBoxLayout()
        scrollbox_layout.addWidget(controlbar)
        scrollbox_layout.addWidget(scroll_area)
        body_rect.setLayout(scrollbox_layout)

        body_layout.addWidget(body_rect)
        self.setLayout(body_layout)

        # register for event filter to listen to
        # return key press
        self.installEventFilter(self)

    def on_cancel_clicked(self):
        """
        Handles when cancel button is clicked
        """
        self.close()
    
    def on_confirm_clicked(self):
        """
        Handles when confirm button is clicked
        """

        # if the window is for adding new block
        # item, get the current tab widget.
        # Otherwise use the current item view
        if self.tab:
            current = self.tab.currentWidget()
        else:
            current = self.item_view

        # get the block item from item view
        block_item = current.get_block_item()
        if block_item is None:
            current.show_error_msg()
            return

        # close the window
        if self.item_changed_handler is not None:
            if self.item_changed_handler(block_item):
                logging.info("Closing LentoBlockItemWindow")
                self.close()
            else:
                logging.info("Not closing LentoBlockItemWindow" \
                    " because block item is not saved")
        else:
            self.close()

    def on_tab_changed(self):
        """
        Handles when tab is changed
        """
        # clear the error message and reload popup list
        current = self.tab.currentWidget()
        current.clear_error_msg()
        current.load_popups()

    def eventFilter(self, obj, event):
        """
        Method called when there is any UI event
        """
        # if return key is pressed, do not dismiss the window
        if event.type() == QtCore.QEvent.KeyPress and obj is self:
            if event.key() == QtCore.Qt.Key_Return:
                return True
        return super().eventFilter(obj, event)
