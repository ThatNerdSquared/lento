import json
import os
import uuid


def create_card():
    new_card = {
        "id": str(uuid.uuid4().hex),
        "name": "Untitled Card",
        "emoji": "😃",
        "time": "0",
        "hard_blocked_sites": {},
        "soft_blocked_sites": {},
        "hard_blocked_apps": {},
        "soft_blocked_apps": {},
        "notifications": {},
        "goals": []
    }

    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    settings["cards"][new_card["name"]] = new_card

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def read_cards():
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)
    return settings['cards']


def delete_card(card_to_delete):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)
    del settings['cards'][card_to_delete]
    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)
