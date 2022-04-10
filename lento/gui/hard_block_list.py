from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget
from lento.common import cards_management as CardsManagement


class HBWebsitesList(QWidget):
    def __init__(self, current_card, HB_LIST, refresh_handler):
        super().__init__()

        self.CURRENT_CARD = current_card
        self.refresh = refresh_handler

        main_layout = QVBoxLayout()

        toggle = QPushButton("Hard-blocked Websites")
        toggle.setCheckable(True)
        toggle.clicked.connect(self.toggle_sublist)

        self.inner_list = QWidget()
        inner_list_layout = QVBoxLayout()
        for item in HB_LIST.keys():
            new_button = QPushButton(item)
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
        print(user_input)
        CardsManagement.add_to_site_blocklists(
            self.CURRENT_CARD,
            "hard_blocked_sites",
            user_input
        )
        self.refresh()
