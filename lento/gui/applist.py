import platform
from PySide6.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget
from lento.common import cards_management as CardsManagement


class AppList(QWidget):
    def __init__(
            self,
            current_card,
            INPUT_LIST,
            current_list_key,
            current_list_title,
            refresh_handler
    ):
        super().__init__()

        self.CURRENT_CARD = current_card
        self.INPUT_LIST = INPUT_LIST
        self.CURRENT_LIST_KEY = current_list_key
        self.refresh = refresh_handler

        main_layout = QVBoxLayout()

        toggle = QPushButton(current_list_title)
        toggle.setObjectName("toggle")
        toggle.setCheckable(True)
        toggle.clicked.connect(self.toggle_sublist)

        self.inner_list = QWidget()
        self.inner_list.setObjectName("innerlist")
        inner_list_layout = QVBoxLayout()
        for item in self.INPUT_LIST.keys():
            new_button = QPushButton(item)

            new_button.setCheckable(True)
            new_button.setChecked(self.INPUT_LIST[item]["enabled"])
            new_button.clicked.connect(self.toggle_site)

            inner_list_layout.addWidget(new_button)

        add_button = QPushButton("+ Add an item")
        add_button.setEnabled(True)
        add_button.clicked.connect(self.prompt_user_for_apps)
        inner_list_layout.addWidget(add_button)

        self.inner_list.setLayout(inner_list_layout)

        main_layout.addWidget(toggle)
        main_layout.addWidget(self.inner_list)
        self.setLayout(main_layout)

    def toggle_sublist(self, checked):
        if checked:
            self.inner_list.show()
        else:
            self.inner_list.hide()

    def add_item(self):
        user_input = self.entry_box.text()
        self.entry_box.clear()
        CardsManagement.add_to_site_blocklists(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            user_input
        )
        self.refresh()

    def toggle_site(self, checked):
        item = self.sender().text()
        self.INPUT_LIST[item]["enabled"] = checked
        CardsManagement.update_app_blocklists(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            self.INPUT_LIST
        )

    def prompt_user_for_apps(self):
        if platform.system() == "Darwin":
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.ExistingFiles)
            dialog.setDirectory("/Applications/")
            dialog.setNameFilter(("Applications (*.app)"))
            if dialog.exec():
                file_names = dialog.selectedFiles()
                CardsManagement.add_to_app_blocklists(
                    self.CURRENT_CARD,
                    self.CURRENT_LIST_KEY,
                    file_names
                )
                self.refresh()
        else:
            print("ow")
