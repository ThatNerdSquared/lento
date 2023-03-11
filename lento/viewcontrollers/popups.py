import logging
from lento import utils
from PySide6 import QtCore
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel  # noqa: E501


class LentoPopUpMode:
    """
    Operating modes of Lento Popup Window
    """
    ERROR = 0
    WARNING = 1


class LentoPopUpWindow(QDialog):
    """
    Popup window 
    """
    def __init__(self, msg, mode=LentoPopUpMode.ERROR):
        """
        Parameters:
        msg: the message to be displayed
        mode: the operating mode of the popup
        """
        super().__init__()

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # set the drop shadow of the popup
        drop_shadow = QGraphicsDropShadowEffect(self)
        drop_shadow.setBlurRadius(20)
        drop_shadow.setOffset(0)
        drop_shadow.setYOffset(4)
        drop_shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(drop_shadow)

        body_layout = QVBoxLayout()

        body_rect = QWidget()
        body_rect_layout = QVBoxLayout()
        body_rect.setLayout(body_rect_layout)
        body_rect.setObjectName("outercard")

        # setup the message with icon
        msg_widget = QWidget()
        msg_widget_layout = QHBoxLayout()
        msg_widget.setLayout(msg_widget_layout)

        img_path = 'assets/error.svg'
        if mode == LentoPopUpMode.WARNING:
            img_path = 'assets/warning.svg'

        img_label = QLabel()
        pixmap = QPixmap(
            utils.get_data_file_path(img_path)
        )
        pixmap = pixmap.scaled(40, 40)
        img_label.setPixmap(pixmap)

        msg_label = QLabel(msg)
        msg_label.setObjectName("popup_window_msg")

        msg_widget_layout.addWidget(img_label)
        msg_widget_layout.addWidget(msg_label)

        # build the options buttons
        button_widget = QWidget()
        button_widget_layout = QHBoxLayout()
        button_widget.setLayout(button_widget_layout)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("popup_cancel_btn")
        cancel_button.clicked.connect(self._on_cancel_clicked)
        
        confirm_button = QPushButton("OK")
        confirm_button.setObjectName("popup_confirm_btn")
        confirm_button.clicked.connect(self._on_confirm_clicked)

        button_widget_layout.addStretch()

        if mode == LentoPopUpMode.WARNING:
            button_widget_layout.addWidget(cancel_button)
            button_widget_layout.addWidget(confirm_button)
        elif mode == LentoPopUpMode.ERROR:
            button_widget_layout.addWidget(confirm_button)

        body_rect_layout.addWidget(msg_widget)
        body_rect_layout.addWidget(button_widget)

        body_layout.addWidget(body_rect)
        self.setLayout(body_layout)

        # register for event filter to listen to
        # return key press
        self.installEventFilter(self)

    def sizeHint(self):
        """
        Provide a suggested size for the popup
        """
        return QSize(300, 50)

    def eventFilter(self, obj, event):
        """
        Method called when there is any UI event
        """
        # if return key is pressed, do not dismiss the popup window
        if event.type() == QtCore.QEvent.KeyPress and obj is self:
            if event.key() == QtCore.Qt.Key_Return:
                return True
        return super().eventFilter(obj, event)

    def _on_cancel_clicked(self):
        """
        Method called when cancel button is clicked
        """
        logging.info("Popup window cancel clicked")
        self.reject()
    
    def _on_confirm_clicked(self):
        """
        Method called when confirm button is clicked
        """
        logging.info("Popup window accept clicked")
        self.accept()
