from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget  # noqa: E501


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
        button = QPushButton("Summon Llama")
        button.setEnabled(True)
        button.clicked.connect(self.add_item)

        layout.addWidget(text)
        layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def add_item(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setDirectory("/Applications/")
        dialog.setNameFilter(("Applications (*.app)"))
        if dialog.exec():
            fileNames = dialog.selectedFiles()
            print(fileNames)


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
