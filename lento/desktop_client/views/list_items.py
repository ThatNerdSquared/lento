import logging
from lento.desktop_client import utils
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QWidget
from lento.desktop_client.viewcontrollers.block_item_window import LentoBlockItemWindow


class LentoListItem(QWidget):
    """
    A single widget that displays a block item in a list as:

    [Icon][Label]        [Edit Button][Delete Button]
    """

    def __init__(self, block_item, edit_handler=None, remove_handler=None):
        """
        Parameters
        block_item: block item to display
        edit_handler: method called when edit button clicked
        remove_handler: method called when remove button clicked
        """
        super().__init__()

        self.block_item = block_item

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        icon = QPushButton()
        icon.setObjectName("list_item_icon")

        # hide icon if block item does not have icon path
        if block_item.icon_path is not None and block_item.icon_path != "":
            icon.setIcon(QIcon(QPixmap(block_item.icon_path)))
        else:
            icon.setVisible(False)

        label = QLabel()
        label.setObjectName("list_item_label")

        # hide label if block item does not have label
        if block_item.label is not None:
            label.setText(block_item.label)
        else:
            label.setVisible(False)

        # build edit button
        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon(utils.get_data_file_path("assets/edit.svg")))
        self.edit_button.clicked.connect(self._on_edit_clicked)
        self.edit_button.setObjectName("list_item_edit_button")

        # set edit button hover image path with asset path
        # relative to the bundle
        edit_hover_path = utils.get_data_file_path("assets/edit_hover.svg")
        self.edit_button.setStyleSheet(
            "#list_item_edit_button:hover {{"
            "image: url({});"
            "}}".format(edit_hover_path)
        )

        # build delete button
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon(utils.get_data_file_path("assets/delete.svg")))
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.delete_button.setObjectName("list_item_delete_button")

        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.setObjectName("list_item")

        self.onItemEdited = edit_handler
        self.onItemRemoved = remove_handler

    def enable(self):
        """
        Enables the control buttons in the list item
        """
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def disable(self):
        """
        Disables the contro buttons in the list item
        """
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def _on_edit_clicked(self):
        """
        Handles when edit button is clicked
        """
        logging.info("Showing edit window for {}".format(self.block_item.label))
        LentoBlockItemWindow(
            block_item=self.block_item, item_changed_handler=self._on_item_changed
        ).exec()

    def _on_delete_clicked(self):
        """
        Handles when delete button is clicked
        """
        logging.info("Delete clicked for {}".format(self.block_item.label))
        if self.onItemRemoved:
            self.onItemRemoved(self)

    def _on_item_changed(self, block_item):
        """
        Method called when the block item of this listitem
        is modified in the LentoBlockItemWindow
        """
        old_block_item = self.block_item
        self.block_item = block_item

        # call handler for when the block item is edited
        if self.onItemEdited:
            self.onItemEdited(self, old_block_item)

        return True
