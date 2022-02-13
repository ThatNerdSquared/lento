import json
import os
import platform
import plistlib
import subprocess
import uuid
from lento.config import Config
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
        "goals": {}
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
    return settings["cards"]


def delete_card(card_to_delete):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)
    del settings["cards"][card_to_delete]
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


def add_to_site_blocklists(card_to_modify, list_to_modify, new_value):
    """Add to either the `hard_blocked_sites` or `soft_blocked_sites` lists."""
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    card_to_mod = settings["cards"][card_to_modify]
    if card_to_mod[list_to_modify] is None:
        raise Exception("List is nonexistent!")
    elif list_to_modify not in [
                "hard_blocked_sites",
                "soft_blocked_sites"
            ]:
        raise Exception("Card field is restricted!")
    elif is_url(new_value) is False:
        raise Exception("URL not valid!")
    elif list_to_modify == "hard_blocked_sites":
        if new_value in card_to_mod["soft_blocked_sites"]:
            raise Exception(f"'{new_value}' already soft blocked!")
    elif list_to_modify == "soft_blocked_sites":
        if new_value in card_to_mod["hard_blocked_sites"]:
            raise Exception(f"'{new_value}' already hard blocked!")

    settings["cards"][card_to_modify][list_to_modify][new_value] = True
    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def update_site_blocklists(card_to_modify, list_to_modify, new_sites_dict):
    """Update one of the blocked_sites lists. Minimal validation."""
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
    elif not isinstance(new_sites_dict, dict):
        raise Exception("new_sites_dict is not a dict!")

    settings["cards"][card_to_modify][list_to_modify] = new_sites_dict
    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def add_to_app_blocklists(card_to_modify, list_to_modify, apps_to_add):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    card = settings["cards"][card_to_modify]

    current_os = platform.system()
    if current_os == "Darwin":
        for app in apps_to_add:
            app_name = os.path.basename(app).replace(".app", "")

            if list_to_modify == "hard_blocked_apps":
                if app_name in card["soft_blocked_apps"]:
                    raise Exception(f"'{app_name}' already soft blocked!")
            elif list_to_modify == "soft_blocked_apps":
                if app_name in card["hard_blocked_apps"]:
                    raise Exception(f"'{app_name}' already hard blocked!")

            bundle_id = subprocess.check_output([
                "mdls",
                "-name",
                "kMDItemCFBundleIdentifier",
                "-r",
                app
            ]).decode("utf-8")

            if app[:14] == "/Applications/":
                app = os.path.join(
                    Config.MACOS_APPLICATION_FOLDER,
                    app_name + ".app"
                )
                plist_path = os.path.join(
                    app,
                    "Contents",
                    "Info.plist"
                )
            else:
                plist_path = os.path.join(app, "Contents", "Info.plist")
            with open(plist_path, "rb") as fp:
                app_plist = plistlib.load(fp)
            icon_name = app_plist["CFBundleIconFile"]
            if icon_name[-5:] != ".icns":
                icon_name = app_plist["CFBundleIconFile"] + ".icns"
            original_icon_path = os.path.join(
                app,
                "Contents",
                "Resources",
                icon_name
            )
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
    elif current_os == "Windows":
        for app in apps_to_add:
            app_name = app["name"]
            if list_to_modify == "hard_blocked_apps":
                if app_name in card["soft_blocked_apps"]:
                    raise Exception(f"'{app_name}' already soft blocked!")
            elif list_to_modify == "soft_blocked_apps":
                if app_name in card["hard_blocked_apps"]:
                    raise Exception(f"'{app_name}' already hard blocked!")
            card[list_to_modify][app["name"]] = {
                "enabled": True,
                "path": app["path"],
                "app_icon_path": app["icon_path"]
            }
    else:
        raise Exception("OS name invalid or not found!")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def update_app_blocklists(card_to_modify, list_to_modify, new_list_structure):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if list_to_modify not in [
                "hard_blocked_apps",
                "soft_blocked_apps"
            ]:
        raise Exception("Card field is restricted!")

    settings["cards"][card_to_modify][list_to_modify] = new_list_structure

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def add_notification(
            name,
            enabled,
            card_to_modify,
            type,
            blocked_visit_triggers,
            associated_goals,
            time_interval_trigger,
            title,
            body,
            audio_paths
        ):
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if not isinstance(name, str):
        raise Exception("Name must be a string!")
    elif not isinstance(enabled, bool):
        raise Exception("Enabled must be a boolean!")
    elif type not in ["banner", "popup", "audio"]:
        raise Exception("Notification type not valid!")
    elif not isinstance(blocked_visit_triggers, list):
        raise Exception("Blocked visit triggers is not a list!")
    for item in blocked_visit_triggers:
        list_checks = (
            item in settings["cards"][card_to_modify]["hard_blocked_sites"],
            item in settings["cards"][card_to_modify]["soft_blocked_sites"],
            item in settings["cards"][card_to_modify]["hard_blocked_apps"],
            item in settings["cards"][card_to_modify]["soft_blocked_apps"],
        )
        if True not in list_checks:
            raise Exception(f"Blocked visit triggers '{item}' not found in blocklists!")  # noqa: E501
    if not isinstance(associated_goals, list):
        raise Exception("Associated goals is not a list!")
    for item in associated_goals:
        if item not in settings["cards"][card_to_modify]["goals"]:
            raise Exception("Associated goals not found in goal list!")
    if not isinstance(time_interval_trigger, int) and time_interval_trigger is not None:  # noqa: E501
        raise Exception("Timer interval trigger is not an integer or None!")
    elif not isinstance(title, str) and title is not None:
        raise Exception("Notification title is not a string!")
    elif not isinstance(body, str) and body is not None:
        raise Exception("Notification body is not a string!")

    new_notif = {
        "name": name,
        "enabled": enabled,
        "type": type,
        "blocked_visit_triggers": blocked_visit_triggers,
        "associated_goals": associated_goals,
        "time_interval_trigger": time_interval_trigger,
        "title": title,
        "body": body,
        "audio_paths": audio_paths
    }

    card = settings["cards"][card_to_modify]
    card["notifications"][str(uuid.uuid4().hex)] = new_notif

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def update_notification_list(card_to_modify, new_notifs_dict):
    """Update notifications for a card. Minimal validation."""
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if not isinstance(new_notifs_dict, dict):
        raise Exception("new_notifs_dict is not a dict!")
    for item in list(new_notifs_dict.keys()):
        is_notif_dict_valid = set(new_notifs_dict[item].keys()) == set([
            "name",
            "enabled",
            "type",
            "blocked_visit_triggers",
            "associated_goals",
            "time_interval_trigger",
            "title",
            "body",
            "audio_paths"
        ])
        if not is_notif_dict_valid:
            raise Exception(f"Notif {item} had invalid structure!")

    settings["cards"][card_to_modify]["notifications"] = new_notifs_dict

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def add_goal(card_to_modify: str, goal_to_add: str) -> None:
    """Add a goal to a card. Automatically adds as disabled."""
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if not isinstance(goal_to_add, str):
        raise Exception("Goal to add is not string!")

    settings["cards"][card_to_modify]["goals"][goal_to_add] = False

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)


def update_goal_list(card_to_modify, new_goals_dict):
    """Update goals for a card. Minimal validation."""
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")
    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    if not isinstance(new_goals_dict, dict):
        raise Exception("new_goals_dict is not a dict!")
    for item in list(new_goals_dict.keys()):
        if not isinstance(new_goals_dict[item], bool):
            raise Exception(f"Goal '{item}' has invalid structure!")

    settings["cards"][card_to_modify]["goals"] = new_goals_dict

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(settings, settings_json)
