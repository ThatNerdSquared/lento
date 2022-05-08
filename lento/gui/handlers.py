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

    def add_site(self, sender):
        user_input = sender.text()
        sender.clear()
        CardsManagement.add_to_site_blocklists(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            user_input
        )
        self.REFRESH()

    def toggle_item(self, sender):
        item = sender.text()
        self.INPUT_LIST[item]["enabled"] = sender.isChecked()
        update_functions = {
            "WebsiteList": CardsManagement.update_site_blocklists,
            "AppList": CardsManagement.update_app_blocklists
        }
        return update_functions[self.LIST_TYPE](
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            self.INPUT_LIST
        )

    def add_apps(self, file_names):
        CardsManagement.add_to_app_blocklists(
            self.CURRENT_CARD,
            self.CURRENT_LIST_KEY,
            file_names
        )
        self.REFRESH()
