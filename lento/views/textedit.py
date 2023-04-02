from PySide6 import QtCore
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QFontMetrics, Qt


class LentoTextEdit(QTextEdit):
    """
    Text edit that grows with input text size and
    is only editable on double click
    """

    def __init__(self, text=None, placeholder=None):
        """
        Parameters:
        text: preset text
        placeholder: placeholder to display when text is empty
        """
        super().__init__()

        self.readonly = False
        self.placeholder = placeholder
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.textChanged.connect(self.onTextChanged)
        # register for event filter to listen to
        # return key press
        self.installEventFilter(self)

        # set initial text edit height
        self.lineHeight = QFontMetrics(self.font()).lineSpacing()
        self.setFixedHeight(3 * self.lineHeight)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if text:
            self.insertPlainText(text)
            self.document().adjustSize()
            size = self.document().size().toSize()
            self.setFixedHeight(size.height())

        if placeholder:
            self.setPlaceholderText(placeholder)

        # method called when text is changed, can be
        # set by the caller
        self.textChangedHandler = None

    def mouseDoubleClickEvent(self, event):
        """
        Method called when mouse is double clicked on this widget
        """
        if not self.readonly:
            self.setReadOnly(False)

    def mousePressEvent(self, event):
        """
        Method called when mouse is pressed
        """
        # do not allow edit on single click of
        # the text edit box
        self.setReadOnly(True)

    def focusInEvent(self, event):
        """
        Method called when cursor is focused on widget
        """
        super().focusInEvent(event)
        self.setPlaceholderText("")

    def focusOutEvent(self, event):
        """
        Method called when cursor is focused out from widget
        """
        # commit the user input text and notify
        # caller/parent of the change in text
        self.setReadOnly(True)

        # only notify text changed if the
        # widget is not in read only mode.
        # If widget is in read only mode, the
        # text would not have been changed
        if not self.readonly:
            if self.textChangedHandler is not None:
                self.textChangedHandler(self.toPlainText())

    def reset(self):
        """
        Reset the text edit state
        """
        self.setText("")
        self.setFixedHeight(3 * self.lineHeight)
        self.setPlaceholderText(self.placeholder)

    def onTextChanged(self):
        """
        Handles when input text is changed
        """
        # reset the height of the text edit
        # according to the size of the input
        # text
        size = self.document().size().toSize()
        self.setFixedHeight(size.height())

    def eventFilter(self, obj, event):
        """
        Method called when there is any UI event
        """
        # if return key is pressed and the current
        # text edit has focus, clear the focus of the
        # text edit. This will trigger focusOutEvent
        # to be called and the text change to be committed
        if event.type() == QtCore.QEvent.KeyPress and obj is self:
            if event.key() == QtCore.Qt.Key_Return and self.hasFocus():
                self.clearFocus()
        return super().eventFilter(obj, event)
