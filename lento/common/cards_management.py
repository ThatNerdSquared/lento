import json
import os
import platform
import plistlib
import subprocess
import uuid
from lento.utils import is_url
from PIL import Image


def create_card():
    new_card = {
        "id": str(uuid.uuid4().hex),
        "name": "Untitled Card",
        "emoji": "😃",
        "time": 0,
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


def update_metadata(card_to_modify, field_to_modify, new_value):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if settings["cards"][card_to_modify][field_to_modify] is None:
        raise Exception("Card field is nonexistent!")
    elif field_to_modify not in ["name", "emoji", "time"]:
        raise Exception("Card field is restricted!")
    elif field_to_modify == "time":
        new_value = float(new_value)

    settings["cards"][card_to_modify][field_to_modify] = new_value
    if field_to_modify == "name":
        new_cards = {
            new_value if k == card_to_modify
            else k: v for k, v in settings["cards"].items()
        }
        settings["cards"] = new_cards

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def update_site_blocklists(card_to_modify, list_to_modify, new_value):
    """Update either the `hard_blocked_sites` or `soft_blocked_sites` lists."""
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if settings["cards"][card_to_modify][list_to_modify] is None:
        raise Exception("List is nonexistent!")
    elif list_to_modify not in [
                "hard_blocked_sites",
                "soft_blocked_sites"
            ]:
        raise Exception("Card field is restricted!")
    elif is_url(new_value) is False:
        raise Exception("URL not valid!")

    settings["cards"][card_to_modify][list_to_modify][new_value] = True
    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def add_to_app_blocklists(card_to_modify, list_to_modify, apps_to_add):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    card = settings["cards"][card_to_modify]

    for app in apps_to_add:
        current_os = platform.system()
        if current_os == "Darwin":
            app_name = app[app.rindex("/")+1:].replace(".app", "")

            bundle_id = subprocess.check_output([
                "mdls",
                "-name",
                "kMDItemCFBundleIdentifier",
                "-r",
                app
            ]).decode("utf-8")

            with open(app + "/Contents/Info.plist", "rb") as fp:
                app_plist = plistlib.load(fp)
            icon_name = app_plist["CFBundleIconFile"]
            if icon_name[-5:] != ".icns":
                icon_name = app_plist["CFBundleIconFile"] + ".icns"
            original_icon_path = app + "/Contents/Resources/" + icon_name
            im = Image.open(original_icon_path)
            rgb_im = im.convert("RGB")

            path_to_save_at = os.path.join(
                    os.path.expanduser("~"),
                    "Library/Application Support/Lento/" + app_name + ".jpg"
                )
            rgb_im.save(path_to_save_at)

            card[list_to_modify][app_name] = {
                "enabled": True,
                "bundle_id": bundle_id,
                "app_icon_path": path_to_save_at
            }

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)
