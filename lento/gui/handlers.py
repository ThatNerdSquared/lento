from lento.common import cards_management as CardsManagement


class Handlers():
    def __init__(
        self,
        current_card,
        current_list_key,
        input_list,
        list_type,
        refresh_handler
    ):
        super().__init__()
        self.CURRENT_CARD = current_card
        self.CURRENT_LIST_KEY = current_list_key
        self.INPUT_LIST = input_list
        self.LIST_TYPE = list_type
        self.REFRESH = refresh_handler

    def add_text_item(self, sender):
        user_input = sender.text()
        sender.clear()
        match self.LIST_TYPE:
            case "GoalList":
                CardsManagement.add_goal(
                    self.CURRENT_CARD,
                    user_input
                )
            case "WebsiteList":
                CardsManagement.add_to_site_blocklists(
                    self.CURRENT_CARD,
                    self.CURRENT_LIST_KEY,
                    user_input
                )
        self.REFRESH()

    def toggle_item(self, sender, entrybox=None):
        item = sender.text()
        if item == "":
            item = entrybox.text()
        try:
            self.INPUT_LIST[item]["enabled"] = sender.isChecked()
        except TypeError:
            self.INPUT_LIST[item] = sender.isChecked()
        match self.LIST_TYPE:
            case "GoalList":
                CardsManagement.update_goal_list(
                    self.CURRENT_CARD,
                    self.INPUT_LIST
                )
            case "WebsiteList":
                CardsManagement.update_site_blocklists(
                    self.CURRENT_CARD,
                    self.CURRENT_LIST_KEY,
                    self.INPUT_LIST
                )
            case "AppList":
                CardsManagement.update_app_blocklists(
                    self.CURRENT_CARD,
                    self.CURRENT_LIST_KEY,
                    self.INPUT_LIST
                )

    def update_editable_item(self, sender, item_index):
        item = sender.text()

        new_list = {}
        i = 0
        for k, v in self.INPUT_LIST.items():
            if item_index == i:
                new_list[item] = v
            else:
                new_list[k] = v
            i += 1
        match self.LIST_TYPE:
            case "GoalList":
                CardsManagement.update_goal_list(
                    self.CURRENT_CARD,
                    self.INPUT_LIST
                )

    def delete_item_handler(self, sender):
        item = sender.text()
        del self.INPUT_LIST[item]
        match self.LIST_TYPE:
            case "GoalList":
                CardsManagement.update_goal_list(
                    self.CURRENT_CARD,
                    self.INPUT_LIST
                )
            case "WebsiteList":
                CardsManagement.update_site_blocklists(
                    self.CURRENT_CARD,
                    self.CURRENT_LIST_KEY,
                    self.INPUT_LIST
                )
        self.REFRESH()

    def add_apps(self, file_names):
        CardsManagement.add_to_app_blocklists(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            file_names
        )
        self.REFRESH()
