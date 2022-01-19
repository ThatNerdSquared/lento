from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget  # noqa: E501


class MainWindow(QMainWindow):
    """The main window for the app."""
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(450, 200))
        self.set_up_window()

    def set_up_window(self):
        self.setWindowTitle("Lento")

        layout = QVBoxLayout()
        text = QLabel("Hello World!")

        layout.addWidget(text)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
