import copy
import json
import os
import platform
import pytest
import subprocess
import uuid
import lento.common.cards_management as CardsManagement
from lento.config import Config
from tests import helpers
from PIL import Image


def test_create_card_uses_correct_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "b0244f7e-8369-49f9-89b4-73811eba3a0e"
    )

    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["initial_blank_config"], settings_json)

    CardsManagement.create_card()

    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    assert settings == helpers.data["bare_config"]


def test_read_cards_returns_correct_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["filled_config"], settings_json)

    expected_result = helpers.data["filled_config"]["cards"]
    cards = CardsManagement.read_cards()
    assert expected_result == cards


def test_delete_card_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["filled_config"], settings_json)

    CardsManagement.delete_card("Llama Taming")
    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    expected_result = helpers.data["bare_config"]
    assert expected_result == new_settings


def test_delete_card_denies_incorrect_card_name(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(KeyError):
        CardsManagement.delete_card("Llama Taming")


def test_update_metadata_changes_nonname_data_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    CardsManagement.update_metadata("Untitled Card", "time", 42)
    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    expected_result = copy.deepcopy(helpers.data["bare_config"])
    expected_result["cards"]["Untitled Card"]["time"] = 42
    assert expected_result == new_settings


def test_update_metadata_changes_name_data_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    CardsManagement.update_metadata(
        "Untitled Card",
        "name",
        "World Domination"
    )
    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    expected_result = helpers.data["updated_bare_config"]
    assert "World Domination" in new_settings["cards"]
    assert expected_result == new_settings


def test_update_metdata_denies_incorrect_card_name_or_field(
            monkeypatch,
            tmp_path
        ):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(KeyError):
        CardsManagement.update_metadata(
            "Llama Training",
            "name",
            "World Domination"
        )

    with pytest.raises(KeyError):
        CardsManagement.update_metadata(
            "Untitled Card",
            "llamas_collected",
            "World Domination"
        )


def test_update_metadata_denies_restricted_field_change(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(Exception):
        CardsManagement.update_metadata(
            "Untitled Card",
            "id",
            "5d15e4f7-e08e-4f91-9713-fa46f13a9761"
        )


def test_update_metadata_validates_time_as_number(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(ValueError):
        CardsManagement.update_metadata(
            "Untitled Card",
            "time",
            "Eternal Reign of the Llama Lords"
        )


def test_update_site_blocklists_adds_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    CardsManagement.update_site_blocklists(
        "Untitled Card",
        "hard_blocked_sites",
        "https://youtube.com"
    )
    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    cards_dict = new_settings["cards"]["Untitled Card"]

    assert "https://youtube.com" in cards_dict["hard_blocked_sites"]
    assert cards_dict["hard_blocked_sites"]["https://youtube.com"] is True


def test_update_site_blocklists_denies_malformed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(Exception, match="URL not valid!"):
        CardsManagement.update_site_blocklists(
            "Untitled Card",
            "hard_blocked_sites",
            "llama"
        )


def test_update_site_blocklists_denies_incorrect_card_or_list_name(
            monkeypatch,
            tmp_path
        ):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(KeyError):
        CardsManagement.update_site_blocklists(
            "Untitled Card",
            "hard_blocked_NIGHTS",
            "https://youtube.com"
        )

    with pytest.raises(KeyError):
        CardsManagement.update_site_blocklists(
            "Llama Taming",
            "hard_blocked_sites",
            "https://youtube.com"
        )


def test_update_site_blocklists_denies_restricted_field_change(
            monkeypatch,
            tmp_path
        ):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(Exception, match="Card field is restricted!"):
        CardsManagement.update_site_blocklists(
            "Untitled Card",
            "hard_blocked_apps",
            "org.zotero.zotero"
        )


def test_update_add_to_app_blocklists_adds_data_darwin(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    folders = {
        "application_support": os.path.join(
            "Library",
            "Application Support",
            "Lento"
        ),
        "apps_folder": "Applications",
        "gris_folders": os.path.join("Applications", "GRIS.app", "Contents"),
        "scrivener_folder": os.path.join(
            "Applications",
            "Scrivener.app",
            "Contents"
        ),
        "nnw_folder": os.path.join(
            "Applications",
            "NetNewsWire.app",
            "Contents"
        )
    }
    for f in folders.keys():
        os.makedirs(os.path.join(tmp_path, folders[f]))

    for file in ["GRIS", "Scrivener", "NetNewsWire"]:
        path = os.path.join(
            tmp_path,
            "Applications",
            file + ".app",
            "Contents",
            "Info.plist"
        )
        plist_file = open(path, "w", encoding="UTF-8")
        plist_file.write(helpers.data[file])
        plist_file.close()

    if platform.system() == "Windows":
        monkeypatch.setattr(
            Config,
            "MACOS_APPLICATION_FOLDER",
            os.path.join(tmp_path, folders["apps_folder"])
        )
    monkeypatch.setattr(Image, "open", lambda x: helpers.fake_image)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(subprocess, "check_output", helpers.fake_bundle_id)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    CardsManagement.add_to_app_blocklists(
        "Untitled Card",
        "hard_blocked_apps",
        [
            "/Applications/GRIS.app",
            "/Applications/Scrivener.app",
            "/Applications/NetNewsWire.app"
        ]
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    hb_list = new_settings["cards"]["Untitled Card"]["hard_blocked_apps"]

    assert "GRIS" in hb_list
    assert "Scrivener" in hb_list
    assert "NetNewsWire" in hb_list

    assert hb_list["GRIS"] == {
        "enabled": True,
        "bundle_id": "unity.nomada studio.GRIS",
        "app_icon_path": os.path.join(
            os.path.expanduser("~"),
            "Library/Application Support/Lento/GRIS.jpg"
        )
    }
    assert hb_list["Scrivener"] == {
        "enabled": True,
        "bundle_id": "com.literatureandlatte.scrivener3",
        "app_icon_path": os.path.join(
            os.path.expanduser("~"),
            "Library/Application Support/Lento/Scrivener.jpg"
        )
    }
    assert hb_list["NetNewsWire"] == {
        "enabled": True,
        "bundle_id": "com.ranchero.NetNewsWire-Evergreen",
        "app_icon_path": os.path.join(
            os.path.expanduser("~"),
            "Library/Application Support/Lento/NetNewsWire.jpg"
        )
    }


@pytest.mark.skip
def test_update_add_to_app_blocklists_adds_data_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    CardsManagement.add_to_app_blocklists(
        "Untitled Card",
        "hard_blocked_apps",
        [
            "Notepad",
            "AutoHotKey",
            "Discord"
        ]
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    hb_list = new_settings["cards"]["Untitled Card"]["hard_blocked_apps"]

    assert "Notepad" in hb_list
    assert "AutoHotKey" in hb_list
    assert "Discord" in hb_list


def test_update_app_blocklists_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_with_apps"], settings_json)

    CardsManagement.update_app_blocklists(
        "Untitled Card",
        "hard_blocked_apps",
        helpers.data["new_blocklist"]
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    new_hblist = new_settings["cards"]["Untitled Card"]["hard_blocked_apps"]
    correct_cards = helpers.data["bare_config_reordered_apps"]["cards"]
    assert new_hblist == correct_cards["Untitled Card"]["hard_blocked_apps"]


def test_update_app_blocklists_rejects_incorrect(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(KeyError):
        CardsManagement.update_app_blocklists(
            "Llama",
            "hard_blocked_apps",
            helpers.data["new_blocklist"]
        )
    with pytest.raises(Exception, match="Card field is restricted"):
        CardsManagement.update_app_blocklists(
            "Untitled Card",
            "hard_blocked_NIGHTS",
            helpers.data["new_blocklist"]
        )
    with pytest.raises(Exception, match="Card field is restricted"):
        CardsManagement.update_app_blocklists(
            "Untitled Card",
            "hard_blocked_sites",
            helpers.data["new_blocklist"]
        )


def test_add_notification_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "a019868e-f43f-478f-8dcc-ba78c35525c4"
    )
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    data = copy.deepcopy(helpers.data["bare_config"])
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["youtube.com"] = True
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["twitter.com"] = True
    data["cards"]["Untitled Card"]["goals"]["Debug USACO problem"] = True
    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(data, settings_json)

    CardsManagement.add_notification(
        "Test Notif 1",
        True,
        "Untitled Card",
        "banner",
        ["youtube.com", "twitter.com"],
        ["Debug USACO problem"],
        None,
        "Get back to %g!",
        "Keep focused!",
        {
            "reminder": "~/Desktop/reminder.mp3",
            "Frog": "/System/Library/Sounds/Frog.aiff"
        }
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    new_notifs = new_settings["cards"]["Untitled Card"]["notifications"]
    correct_cards = helpers.data["bare_config_with_notif"]["cards"]
    assert new_notifs == correct_cards["Untitled Card"]["notifications"]


def test_add_notification_rejects_incorrect_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "a019868e-f43f-478f-8dcc-ba78c35525c4"
    )
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    data = copy.deepcopy(helpers.data["bare_config"])
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["youtube.com"] = True
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["twitter.com"] = True
    data["cards"]["Untitled Card"]["goals"]["Debug USACO problem"] = True
    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(data, settings_json)

    with pytest.raises(Exception, match="Name must be a string!"):
        CardsManagement.add_notification(
            42,
            True,
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(Exception, match="Enabled must be a boolean!"):
        CardsManagement.add_notification(
            "Test Notif 1",
            "Llama",
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(KeyError):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Llama",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(Exception, match="Notification type not valid!"):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "llama_army",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(
                Exception,
                match="Blocked visit triggers is not a list!"
            ):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            "youtube.com",
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(
                Exception,
                match="Blocked visit triggers 'thesephist.com' not found in blocklists!"  # noqa: E501
            ):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            ["thesephist.com"],
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(Exception, match="Associated goals is not a list!"):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            "Debug USACO problem",
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(
                Exception,
                match="Associated goals not found in goal list!"
            ):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Amass gigantic fleet of llamas"],
            None,
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(
                Exception,
                match="Timer interval trigger is not an integer or None!"
            ):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            "Llama",
            "Get back to %g!",
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(
                Exception,
                match="Notification title is not a string!"
            ):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            None,
            42,
            "Keep focused!",
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )
    with pytest.raises(
                Exception,
                match="Notification body is not a string!"
            ):
        CardsManagement.add_notification(
            "Test Notif 1",
            True,
            "Untitled Card",
            "banner",
            ["youtube.com", "twitter.com"],
            ["Debug USACO problem"],
            None,
            "Get back to %g!",
            42,
            {
                "reminder": "~/Desktop/reminder.mp3",
                "Frog": "/System/Library/Sounds/Frog.aiff"
            }
        )


def test_update_notification_list_reorders_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_multiple_notif"], settings_json)

    CardsManagement.update_notification_list(
        "Untitled Card",
        helpers.data["reordered_notifs_dict"]
    )
    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    card_notif_dict = new_settings["cards"]["Untitled Card"]["notifications"]

    assert "a019868e-f43f-478f-8dcc-ba78c35525c4" in card_notif_dict
    assert "2d189b37-6eaf-478f-a5ab-e19c9dab5738" in card_notif_dict

    assert card_notif_dict["a019868e-f43f-478f-8dcc-ba78c35525c4"] == {
        "name": "Test Notif 1",
        "enabled": True,
        "type": "banner",
        "blocked_visit_triggers": [
            "youtube.com",
            "twitter.com"
        ],
        "associated_goals": [
            "Debug USACO problem"
        ],
        "time_interval_trigger": None,
        "title": "Get back to %g!",
        "body": "Keep focused!",
        "audio_paths": {
            "reminder": "~/Desktop/reminder.mp3",
            "Frog": "/System/Library/Sounds/Frog.aiff"
        }
    }
    assert card_notif_dict["2d189b37-6eaf-478f-a5ab-e19c9dab5738"] == {
        "name": "Test Notif 2",
        "enabled": False,
        "type": "popup",
        "blocked_visit_triggers": [],
        "associated_goals": [
            "Create pet AI"
        ],
        "time_interval_trigger": 900000,
        "title": "Work on %g",
        "body": "Keep focused!",
        "audio_paths": {
            "Bloop": "/System/Library/Sounds/Bloop.aiff"
        }
    }

    assert list(card_notif_dict.keys()) == [
        "2d189b37-6eaf-478f-a5ab-e19c9dab5738",
        "a019868e-f43f-478f-8dcc-ba78c35525c4"
    ]


def test_update_notification_list_deletes_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_multiple_notif"], settings_json)

    CardsManagement.update_notification_list(
        "Untitled Card",
        helpers.data["deleted_notifs_dict"]
    )
    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    card_notif_dict = new_settings["cards"]["Untitled Card"]["notifications"]

    assert "a019868e-f43f-478f-8dcc-ba78c35525c4" not in card_notif_dict
    assert "2d189b37-6eaf-478f-a5ab-e19c9dab5738" in card_notif_dict

    assert card_notif_dict["2d189b37-6eaf-478f-a5ab-e19c9dab5738"] == {
        "name": "Test Notif 2",
        "enabled": False,
        "type": "popup",
        "blocked_visit_triggers": [],
        "associated_goals": [
            "Create pet AI"
        ],
        "time_interval_trigger": 900000,
        "title": "Work on %g",
        "body": "Keep focused!",
        "audio_paths": {
            "Bloop": "/System/Library/Sounds/Bloop.aiff"
        }
    }

    assert list(card_notif_dict.keys()) == [
        "2d189b37-6eaf-478f-a5ab-e19c9dab5738",
    ]


def test_update_notification_list_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_multiple_notif"], settings_json)

    with pytest.raises(Exception, match="new_notifs_dict is not a dict!"):
        CardsManagement.update_notification_list(
            "Untitled Card",
            "Llama"
        )
    with pytest.raises(
                Exception,
                match="Notif 2d189b37-6eaf-478f-a5ab-e19c9dab5738 had invalid structure!"  # noqa: E501
            ):
        CardsManagement.update_notification_list(
            "Untitled Card",
            helpers.data["flawed_notifs_dict"]
        )


def test_add_goal_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    CardsManagement.add_goal(
        "Untitled Card",
        "Conquer world"
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    new_goals_dict = new_settings["cards"]["Untitled Card"]["goals"]
    assert "Conquer world" in new_goals_dict
    assert new_goals_dict["Conquer world"] is False


def test_add_goal_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config"], settings_json)

    with pytest.raises(Exception, match="Goal to add is not string!"):
        CardsManagement.add_goal(
            "Untitled Card",
            42
        )
    with pytest.raises(KeyError):
        CardsManagement.add_goal(
            42,
            "Conquer world"
        )


def test_update_goal_list_reorders_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_with_goals"], settings_json)

    CardsManagement.update_goal_list(
        "Untitled Card",
        helpers.data["reordered_goal_dict"]
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    card_goals_dict = new_settings["cards"]["Untitled Card"]["goals"]

    assert "Conquer world" in card_goals_dict
    assert "Debug USACO problem" in card_goals_dict
    assert card_goals_dict["Conquer world"] is False
    assert card_goals_dict["Debug USACO problem"] is True


def test_update_goal_list_deletes_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_with_goals"], settings_json)

    CardsManagement.update_goal_list(
        "Untitled Card",
        {"Conquer world": False}
    )

    with open(path, "r", encoding="UTF-8") as settings_json:
        new_settings = json.load(settings_json)

    card_goals_dict = new_settings["cards"]["Untitled Card"]["goals"]

    assert "Conquer world" in card_goals_dict
    assert "Debug USACO problem" not in card_goals_dict
    assert card_goals_dict["Conquer world"] is False
    assert list(card_goals_dict.keys()) == ["Conquer world"]


def test_update_goal_list_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    with open(path, "w", encoding="UTF-8") as settings_json:
        json.dump(helpers.data["bare_config_with_goals"], settings_json)

    with pytest.raises(Exception):
        CardsManagement.update_goal_list(
            "Untitled Card",
            "Llama"
        )
    with pytest.raises(Exception):
        CardsManagement.update_goal_list(
            "Llama",
            helpers.data["reordered_goal_dict"]
        )
