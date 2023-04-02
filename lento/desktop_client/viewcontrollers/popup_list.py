import logging
import uuid
from PySide6.QtWidgets import QWidget, QVBoxLayout
from lento.desktop_client.views.popup_entry import LentoPopupEntry
from lento.desktop_client.model.block_items import LentoPopUpItem
from lento.desktop_client.viewcontrollers.popups import LentoPopUpWindow, LentoPopUpMode


class LentoPopUpList(QWidget):
    """
    Widget that displays and manages the list of
    selectable custom popup messages
    """

    def __init__(self):
        super().__init__()

        self.popup_item_list = None
        self.selectedPopupID = None
        self.defaultEntry = None
        self.layout = QVBoxLayout()

        self.updatePopups()
        self.setLayout(self.layout)

    def updatePopups(self):
        """
        Updates the list of popup messages from lento settings
        """

        logging.info("Updating popup message list")
        # delete all existing popup messages
        self.clearPopup()
        # read the list of popup messages from lento settings
        self.popup_item_list = LentoPopUpItem.get_popup_items_list()

        # add the default entry
        self.defaultEntry = self._addEntry(editable=False)
        self.defaultEntry.textEdit.insertPlainText("Use Default Popup")

        # add each popup message entry to list
        for popup_item in self.popup_item_list:
            self._addEntry(popup_item=popup_item)

        # add new entry to allow new pop ups to be added
        self._addEntry()

        # reselect the selected pop up message
        self.selectPopup(self.selectedPopupID)

    def selectPopup(self, popup_id):
        """
        Selects the pop up message with provided popup ID

        Returns:
        True if the popup message with provided ID is found
        False otherwise
        """
        # deselect any selected entry first
        selected = self.selectedEntry()
        if selected is not None:
            selected.deselect()

        # if provided popup ID is None, select
        # the default message
        if popup_id is None:
            logging.info("Selecting default popup message")
            self.selectedPopupID = None
            self.defaultEntry.select()
            return True

        # find and select the entry with the ID
        for i in range(self.layout.count()):
            entry = self.layout.itemAt(i).widget()
            if entry.popup_id() == popup_id:
                logging.info("Selecting popup message with id {}".format(popup_id))
                self.selectedPopupID = popup_id
                entry.select()
                return True

        # if no entry is found, select the deafult
        # entry
        logging.info(
            "Cannot find popup message with id {},"
            " selecting default message".format(popup_id)
        )
        self.defaultEntry.select()
        self.selectedPopupID = None
        return False

    def selectedPopup(self):
        """
        Returns the selected popup message item
        """
        entry = self.selectedEntry()
        return entry.popup_item if entry else None

    def selectedEntry(self):
        """
        Returns the selected LentoPopupEntry
        """

        # if no selected popup ID saved, return
        # default entry
        if self.selectedPopupID is None:
            return self.defaultEntry

        # find the selected popup ID and return
        # if found
        for i in range(self.layout.count()):
            entry = self.layout.itemAt(i).widget()
            if entry.popup_id() == self.selectedPopupID:
                return entry

        # if selected popup ID is not found,
        # return None
        self.selectedPopupID = None
        return None

    def _addEntry(self, popup_item=None, editable=True):
        """
        Adds a new empty popup message entry to the list

        Parameters:
        popup_item: the popup item to be contained in the entry
        editable: whether this entry will be editable
        """
        newEntry = LentoPopupEntry(
            editable=editable,
            popup_item=popup_item,
            placeholder="Double Click to Add/Edit Custom Popup...",
        )
        newEntry.selectedHandler = self._handleEntrySelected
        newEntry.textInputHandler = self._handleEntryTextInput
        self.layout.addWidget(newEntry)

        return newEntry

    def clearPopup(self):
        """
        Delete all popup items in the list
        """
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clearLayout(item.layout())

    def _handleEntrySelected(self, entry):
        """
        Handles when a popup message entry is selected

        Parameters:
        entry: the LentoPopupEntry object selected
        """

        # if the popup id is already selected, do nothing
        if self.selectedPopupID == entry.popup_id():
            return

        # if the popup message in the entry is not empty,
        # select the entry
        entryText = entry.textEdit.toPlainText()
        if len(entryText) > 0:
            self.selectPopup(entry.popup_id())

    def _handleEntryTextInput(self, entry, new_text):
        """
        Handles when new text is inputted into LentoPopupEntry

        Parameters:
        entry: the LentoPopupEntry object with text changed
        new_text: the new text inputted
        """

        entry_to_remove = None
        # if the new text is empty, that indicates that
        # the popup entry is being deleted. Otherwise
        # consider the operation as an edit
        is_edit = len(new_text) > 0
        # if the entry does not contain any popup
        # item, consider this operation as adding
        # new popup message
        is_add_new = entry.popup_item is None

        if is_edit:
            if '"' in new_text:
                LentoPopUpWindow(
                    'Custom popup message does not support double quote (")',
                    mode=LentoPopUpMode.ERROR,
                ).exec()
                if is_add_new:
                    entry.textEdit.reset()
                else:
                    entry.textEdit.setText(entry.popup_item.msg)
                return

            # enable the checkbox
            entry.checkBox.setEnabled(True)

            # if adding new popup message, create new
            # popup item
            if is_add_new:
                entry.popup_item = LentoPopUpItem(
                    id=str(uuid.uuid4().hex), msg=new_text
                )
            else:
                if entry.popup_item.msg == new_text:
                    return

                ret = LentoPopUpWindow(
                    "Change to this popup message will be applied "
                    "to all other cards & block items, OK to continue?",
                    mode=LentoPopUpMode.WARNING,
                ).exec()

                if ret == 0:
                    entry.textEdit.setText(entry.popup_item.msg)
                    return

            # update the popup message and save it to
            # lento settings
            entry.popup_item.update_msg(new_text)
        else:
            # if the text change applies to a new popup
            # entry, simply reset it since it does not
            # contain any pop item to delete
            if is_add_new:
                entry.textEdit.reset()
                return
            else:
                # display warning popup window confirming
                # deletion
                ret = LentoPopUpWindow(
                    "Deletion of this popup message will be applied "
                    "to all other cards & block items, OK to continue?",
                    mode=LentoPopUpMode.WARNING,
                ).exec()

                if ret == 0:
                    entry.textEdit.setText(entry.popup_item.msg)
                    return

            # delete the popup item
            entry.popup_item.delete()

        # find the popup entry widget in the list
        # and adjust the list according to the
        # change in the entry
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget is entry:
                if is_edit:
                    # if the entry is edited and
                    # and it is the last one in the
                    # list, add new entry to allow
                    # new popup to be added
                    if i == self.layout.count() - 1:
                        self._addEntry()
                else:
                    # if the entry is being deleted
                    # and it is not the last one in
                    # the list, remove it
                    if i != self.layout.count() - 1:
                        entry_to_remove = entry
                break

        # remove the popup entry to be removed, note that
        # we do not remove the entry in the above loop as
        # the entry is part of the list and moving from
        # list while iterating may cause problems
        if entry_to_remove:
            self.layout.removeWidget(entry_to_remove)
            entry_to_remove.setParent(None)
