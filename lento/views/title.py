from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QWidget

# TODO: make the title respond to focus out


class LentoCardTitle(QWidget):
    """
    Card Title Widget
    """

    def __init__(self, text, text_changed_handler):
        """
        Parameters:
        text: the text to display
        text_changed_handler: method called when title text is changed
        """
        super().__init__()

        self.text_changed_handler = text_changed_handler

        title_layout = QHBoxLayout()

        self.title = QLineEdit(text)
        self.title.returnPressed.connect(self.on_return_pressed)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("cardtitle")

        title_layout.addWidget(self.title)
        self.setLayout(title_layout)

    def on_return_pressed(self):
        """
        Method called when return is pressed
        """
        # clears focus of the edit box and
        # update title
        self.title.clearFocus()
        self.title_updated()

    def title_updated(self):
        """
        Handles when title text is updated
        """
        # remove the leading and trailing spaces
        user_input = self.title.text()
        user_input = str.strip(user_input)
        self.title.setText(user_input)

        # notify title text change
        self.text_changed_handler(user_input)
