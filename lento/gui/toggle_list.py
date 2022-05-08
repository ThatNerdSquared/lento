from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from lento.gui.components.list_items import AppPicker, EditableListItem, TextEntryAdder, LauncherListItem  # noqa: E501
from lento.gui.handlers import Handlers


class ToggleList(QWidget):
    def __init__(
            self,
            current_card,
            INPUT_LIST,
            current_list_key,
            current_list_title,
            list_type,
            refresh_handler
    ):
        super().__init__()

        self.CURRENT_CARD = current_card
        self.INPUT_LIST = INPUT_LIST
        self.CURRENT_LIST_KEY = current_list_key
        self.LIST_TYPE = list_type
        self.refresh = refresh_handler

        main_layout = QVBoxLayout()

        toggle = QPushButton(current_list_title)
        toggle.setObjectName("toggle")
        toggle.setCheckable(True)
        toggle.clicked.connect(self.toggle_sublist)

        handlers = Handlers(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            self.INPUT_LIST,
            self.LIST_TYPE,
            self.refresh
        )

        self.inner_list = QWidget()
        self.inner_list.setObjectName("innerlist")
        inner_list_layout = QVBoxLayout()
        inner_list_layout.setSpacing(0)
        i = 0
        for item in self.INPUT_LIST.keys():
            match self.LIST_TYPE:
                case "GoalList":
                    list_item = EditableListItem(
                        item,
                        self.INPUT_LIST[item],
                        handlers.update_editable_item,
                        handlers.toggle_item,
                        handlers.delete_item_handler,
                        i
                    )
                case "WebsiteList":
                    list_item = LauncherListItem(
                        item,
                        self.INPUT_LIST[item]["enabled"],
                        handlers.toggle_item,
                        handlers.delete_item_handler,
                        False
                    )
                case "AppList":
                    list_item = LauncherListItem(
                        item,
                        self.INPUT_LIST[item]["enabled"],
                        handlers.toggle_item,
                        handlers.delete_item_handler,
                        False
                    )
                case _:
                    list_item = QLabel("An error occured: no list type found")
            inner_list_layout.addWidget(list_item)
            i += 1

        match self.LIST_TYPE:
            case "GoalList":
                adder_item = TextEntryAdder(
                    "Add a goal...",
                    handlers.add_text_item
                )
            case "WebsiteList":
                adder_item = TextEntryAdder(
                    "Add a site...",
                    handlers.add_text_item
                )
            case "AppList":
                adder_item = AppPicker(
                    self.CURRENT_CARD,
                    self.CURRENT_LIST_KEY,
                    handlers.add_apps
                )
            case _:
                adder_item = QLabel("An error occured: no list type found")
        inner_list_layout.addWidget(adder_item)
        self.inner_list.setLayout(inner_list_layout)

        main_layout.addWidget(toggle)
        main_layout.addWidget(self.inner_list)
        self.setLayout(main_layout)

    def toggle_sublist(self, checked):
        if checked:
            self.inner_list.show()
        else:
            self.inner_list.hide()
