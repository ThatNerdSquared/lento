import sys
from lento.gui.card import Card
from lento import utils
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton  # noqa: E501
from lento.common import cards_management as CardsManagement


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lento")
        self.set_up_window()

    def set_up_window(self):
        main = QWidget()
        main_layout = QHBoxLayout()
        main.setLayout(main_layout)

        self.left_button = QPushButton()
        main_layout.addWidget(self.left_button)

        cards = CardsManagement.read_cards()
        for item in cards.keys():
            _card = Card(cards[item], self.refresh_event)
            main_layout.addWidget(_card)

        self.right_button = QPushButton()
        main_layout.addWidget(self.right_button)
        self.setCentralWidget(main)

    def refresh_event(self):
        self.set_up_window()


def main():
    app = QApplication(sys.argv)
    stylesheet_path = Path(utils.get_data_file_path("lento.qss"))
    app.setStyleSheet(stylesheet_path.read_text())
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
