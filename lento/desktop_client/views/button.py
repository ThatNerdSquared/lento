from lento.desktop_client import utils
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class LentoOneTimeButton(QPushButton):
    """
    Button that is disabled after click
    """

    def __init__(self, unclicked_text, clicked_text, on_click_handler):
        """
        Parameters:
        unclicked_text: text to display when button is unclicked
        clicked_text: text to display when button is clicked
        on_click_handler: method called when button is clicked
        """
        super().__init__()
        self.unclicked_text = unclicked_text
        self.clicked_text = clicked_text
        self.on_click_handler = on_click_handler

        self.clicked.connect(self._on_click)
        self.setObjectName("startbutton")
        self.reset()

    def reset(self):
        """
        Reset the button to be clickable
        """
        self.setEnabled(True)
        self.setText(self.unclicked_text)
        self.setIcon(QIcon())

    def activate(self):
        """
        Set the button to be activated
        """
        self.setEnabled(False)
        self.setText(self.clicked_text)
        self.setIcon(QIcon(utils.get_data_file_path("assets/check.svg")))

    def _on_click(self):
        """
        Method called when button is clicked
        """
        self.on_click_handler()
