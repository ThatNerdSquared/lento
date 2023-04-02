import logging
from lento import utils
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from lento.views.list_items import LentoListItem


class LentoToggleList(QWidget):
    """
    Widget displaying a list of items that can be expanded
    or strinked
    """

    def __init__(
        self,
        title,
        item_edited_handler=None,
        item_removed_handler=None,
        resize_handler=None,
    ):
        """
        Parameters:
        title: title of the list
        item_edited_handler: method called when list item is edited
        item_removed_handler: method called when list is removed
        resize_handler: method called when list is resized
        """
        super().__init__()

        self.onItemEdited = item_edited_handler
        self.onItemRemoved = item_removed_handler
        self.onSizeChange = resize_handler

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(0, 0, 0, 10)

        # set up the button to expand and shrink the list
        self.toggle = QPushButton(title)
        self.toggle.setObjectName("toggle")
        self.toggle.setCheckable(True)
        self.toggle.clicked.connect(self._toggle_sublist)
        self.toggle.setMinimumHeight(30)
        self.toggle.setIcon(
            QIcon(utils.get_data_file_path("assets/toggle-unfolded.svg"))
        )

        # set up the inner list with items
        self.inner_list = QWidget()
        self.inner_list.setObjectName("widgetbox")
        self.inner_list_layout = QVBoxLayout()
        self.inner_list_layout.setContentsMargins(0, 5, 0, 5)
        self.inner_list_layout.setSpacing(0)
        self.inner_list.setLayout(self.inner_list_layout)

        self.main_layout.addWidget(self.toggle)
        self.main_layout.addWidget(self.inner_list)
        self.setLayout(self.main_layout)

    def enable(self):
        """
        Enable all list items in the list
        """
        for i in range(self.inner_list_layout.count()):
            list_item = self.inner_list_layout.itemAt(i).widget()
            list_item.enable()

    def disable(self):
        """
        Disable all list items in the list
        """
        for i in range(self.inner_list_layout.count()):
            list_item = self.inner_list_layout.itemAt(i).widget()
            list_item.disable()

    def count(self):
        """
        Returns:
        number of elements in the list
        """
        return self.inner_list_layout.count()

    def list_height(self, parent_widget):
        """
        Parameters:
        parent_widget: parent widget containing the list,
            this is used to determine list visibility

        Returns:
        the height of the list in a parent widget
        """
        if not self.isVisibleTo(parent_widget):
            return 0

        return int(self.sizeHint().height())

    def add_to_list(self, block_item):
        """
        Adds a block item to the list
        """
        list_item = LentoListItem(
            block_item,
            edit_handler=self._on_list_item_edited,
            remove_handler=self._on_list_item_removed,
        )
        self.inner_list_layout.addWidget(list_item)

    def remove_from_list(self, block_item):
        """
        Removes a block item from the list
        """
        for i in range(self.inner_list_layout.count()):
            widget = self.inner_list_layout.itemAt(i).widget()

            if widget is not None and isinstance(widget, LentoListItem):
                if widget.block_item.label == block_item.label:
                    # if the widget's block item label
                    # matches the block item label to delete,
                    # remove it from list
                    logging.info(
                        "Removing toggle list item"
                        " with label {}".format(block_item.label)
                    )
                    widget.deleteLater()
                    widget.setParent(None)

                    if self.onItemRemoved:
                        self.onItemRemoved(self, block_item)

                    # must break out of loop and not let
                    # the loop continue because after deletion
                    # the number of widget in inner list layout
                    # has changed
                    break

    def _toggle_sublist(self, checked):
        """
        Method called when toggle button is clicked
        """
        if checked:
            # if toggle button is checked, show inner list
            self.inner_list.show()
            self.toggle.setIcon(
                QIcon(utils.get_data_file_path("assets/toggle-unfolded.svg"))
            )
        else:
            # if toggle button is unchecked, hide inner list
            self.inner_list.hide()
            self.toggle.setIcon(
                QIcon(utils.get_data_file_path("assets/toggle-folded.svg"))
            )

        if self.onSizeChange is not None:
            self.onSizeChange(self)

    def _on_list_item_edited(self, list_item, old_block_item):
        """
        Handles when list item is edited
        """

        # notify caller/parent that list item is edited
        if self.onItemEdited:
            self.onItemEdited(self, old_block_item, list_item.block_item)

    def _on_list_item_removed(self, list_item):
        """
        Handles when list item is removed
        """

        # remove the item from list
        list_item.deleteLater()
        list_item.setParent(None)

        # notify caller/parent that list item is removed
        if self.onItemRemoved:
            self.onItemRemoved(self, list_item.block_item)
