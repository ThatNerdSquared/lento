from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout

from lento.desktop_client import utils
from lento.desktop_client.views.textedit import LentoTextEdit


class LentoPopupEntry(QFrame):
    """
    Widget that displays a popup message entry
    """

    def __init__(self, editable=True, popup_item=None, placeholder=None):
        """
        Parameters:
        editable: whether the entry is editable
        popup_item: the popup_item to display
        placeholder: placeholder text
        """
        super().__init__()
        self.popup_item = popup_item
        text = self.popup_item.msg if self.popup_item is not None else None

        layout = QHBoxLayout()

        self.checkBox = QCheckBox()
        self.checkBox.stateChanged.connect(self._onCheckboxChanged)

        # set up check box icon, note that because the path
        # are relative, the absolute path needs to be determined
        # and added to the style sheet
        checkbox_checked_path = utils.get_data_file_path("assets/checkbox_checked.svg")
        checkbox_normal_path = utils.get_data_file_path("assets/checkbox_normal.svg")
        checkbox_hover_path = utils.get_data_file_path("assets/checkbox_hover.svg")
        checkbox_disabled_path = utils.get_data_file_path(
            "assets/checkbox_disabled.svg"
        )

        self.checkBox.setStyleSheet(
            "QCheckBox::indicator:checked {{"
            "image: url({});"
            "}}"
            "QCheckBox::indicator:unchecked {{"
            "image: url({});"
            "}}"
            "QCheckBox::indicator:unchecked:hover {{"
            "image: url({});"
            "}}"
            "QCheckBox::indicator:unchecked:disabled {{"
            "image: url({});"
            "}}".format(
                checkbox_checked_path,
                checkbox_normal_path,
                checkbox_hover_path,
                checkbox_disabled_path,
            )
        )

        if editable:
            self.checkBox.setEnabled(False)
        else:
            self.checkBox.setEnabled(True)

        layout.addWidget(self.checkBox)

        self.editable = editable
        self.textEdit = LentoTextEdit(text=text, placeholder=placeholder)

        # enable the check box if there is text to be displayed
        if text is not None:
            self.checkBox.setEnabled(True)

        self.textEdit.textChangedHandler = self._onTextChanged
        self.textEdit.readonly = not editable
        layout.addWidget(self.textEdit)

        self.setLayout(layout)
        self.selectedHandler = None
        self.textInputHandler = None

    def popup_id(self):
        """
        Return:
        popup ID of the displayed popup item,
        None if the entry does not contain a popup item
        """
        if self.popup_item:
            return self.popup_item.id

        return None

    def select(self):
        """
        Selects the entry
        """
        self.setStyleSheet(
            "LentoPopupEntry {background-color: #be82f8; border-radius: 8px;}"
        )
        # setting check box as checked will trigger
        # a check box state change and cause
        # _onCheckboxChanged to be called which will
        # make the text edit readonly
        self.checkBox.setChecked(True)

    def deselect(self):
        """
        Deselects the entry
        """
        self.setStyleSheet(
            "LentoPopupEntry {background-color: white; border-radius: 8px;}"
        )
        # setting check box as unchecked will trigger
        # a check box state change and cause
        # _onCheckboxChanged to be called which will
        # reset text edit according to editability
        self.checkBox.setChecked(False)

    def setPlaceHolderText(self, text):
        """
        Set the placeholder text of the text edit
        """
        self.textEdit.setPlaceholderText(text)

    def _onCheckboxChanged(self, int):
        """
        Method called when check box state is changed
        """
        # make the text edit read only if check box
        # is check and reset text edit editability
        # if the check box is unchecked
        if self.checkBox.isChecked():
            self.textEdit.readonly = True
        else:
            self.textEdit.readonly = not self.editable

        if self.selectedHandler is not None:
            self.selectedHandler(self)

    def _onTextChanged(self, text):
        """
        Method called when input text to text edit
        is changed
        """
        # strip the leading and trailing spaces of
        # the string
        text = str.strip(text)
        if self.textInputHandler is not None:
            self.textInputHandler(self, text)
