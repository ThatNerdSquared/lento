import sys
from lento.gui.card import Card
from lento import utils
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton  # noqa: E501


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lento")

        main = QWidget()
        main_layout = QHBoxLayout()
        main.setLayout(main_layout)

        self.left_button = QPushButton()
        self.right_button = QPushButton()
        _card = Card()
        main_layout.addWidget(self.left_button)
        main_layout.addWidget(_card.render_card())
        main_layout.addWidget(self.right_button)

        self.setCentralWidget(main)


def main():
    app = QApplication(sys.argv)
    stylesheet_path = Path(utils.get_data_file_path("lento.qss"))
    app.setStyleSheet(stylesheet_path.read_text())
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
