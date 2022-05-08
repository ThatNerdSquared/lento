import platform
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QWidget  # noqa: E501


class ToggledListItem(QWidget):
    def __init__(self, item_text, is_checked, toggle_handler):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        core_button = QPushButton(item_text)

        core_button.setCheckable(True)
        core_button.setChecked(is_checked)
        core_button.clicked.connect(lambda: toggle_handler(core_button))

        main_layout.addWidget(core_button)
        self.setLayout(main_layout)


class TextEntryAdder(QWidget):
    def __init__(self, item_add_handler):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        entry_box = QLineEdit()
        entry_box.setPlaceholderText("Add a site...")
        entry_box.returnPressed.connect(lambda: item_add_handler(entry_box))

        main_layout.addWidget(entry_box)
        self.setLayout(main_layout)


class AppPicker(QWidget):
    def __init__(self, current_card, current_list_key, add_apps):
        super().__init__()
        self.CURRENT_CARD = current_card
        self.CURRENT_LIST_KEY = current_list_key
        self.add_apps_handler = add_apps

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        core_button = QPushButton("+ Add an app")
        core_button.setEnabled(True)
        core_button.clicked.connect(self.show_app_picker)

        main_layout.addWidget(core_button)
        self.setLayout(main_layout)

    def show_app_picker(self):
        match platform.system():
            case "Darwin":
                self.macos_picker()
            case "Windows":
                self.windows_picker()
            case _:
                raise Exception(f"Platform '{platform.system}' not found!")

    def macos_picker(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setDirectory("/Applications/")
        dialog.setNameFilter(("Applications (*.app)"))
        if dialog.exec():
            self.add_apps_handler(dialog.selectedFiles())

    def windows_picker(self):
        print("ow")
