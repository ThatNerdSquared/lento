from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget
from lento.common import cards_management as CardsManagement


class WebsiteList(QWidget):
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
        toggle.setCheckable(True)
        toggle.clicked.connect(self.toggle_sublist)

        self.inner_list = QWidget()
        inner_list_layout = QVBoxLayout()
        for item in self.INPUT_LIST.keys():
            new_button = QPushButton(item)

            new_button.setCheckable(True)
            new_button.setChecked(self.INPUT_LIST[item])
            new_button.clicked.connect(self.toggle_site)

            inner_list_layout.addWidget(new_button)

        self.entry_box = QLineEdit()
        self.entry_box.returnPressed.connect(self.add_item)

        inner_list_layout.addWidget(self.entry_box)
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
        self.INPUT_LIST[item] = checked
        CardsManagement.update_site_blocklists(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            self.INPUT_LIST
        )
