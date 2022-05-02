import copy
import json
import platform
import pytest
import subprocess
import uuid
import lento.common.cards_management as CardsManagement
from lento.config import Config
from tests import helpers
from pathlib import Path
from PIL import Image
from unittest.mock import MagicMock


def test_create_card_uses_correct_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "b0244f7e-8369-49f9-89b4-73811eba3a0e"
    )

    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["initial_blank_config"]
    ))

    return_val = CardsManagement.create_card(0)

    result = json.loads(Config.SETTINGS_PATH.read_text())

    assert result == helpers.data["config_after_add"]
    assert result["cards"][return_val]["name"] == "Untitled Card 1"
    assert return_val == "Untitled Card 1"


def test_read_cards_returns_correct_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["filled_config"]
    ))

    expected_result = helpers.data["filled_config"]["cards"]
    cards = CardsManagement.read_cards()
    assert expected_result == cards


def test_delete_card_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["filled_config"]
    ))

    CardsManagement.delete_card("Llama Taming")
    result = json.loads(Config.SETTINGS_PATH.read_text())

    expected_result = helpers.data["bare_config"]
    assert expected_result == result


def test_delete_card_denies_incorrect_card_name(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(KeyError, match="Llama Taming"):
        CardsManagement.delete_card("Llama Taming")


def test_update_metadata_changes_nonname_data_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    CardsManagement.update_metadata("Untitled Card", "time", 42)
    result = json.loads(Config.SETTINGS_PATH.read_text())

    expected_result = copy.deepcopy(helpers.data["bare_config"])
    expected_result["cards"]["Untitled Card"]["time"] = 42
    assert expected_result == result


def test_update_metadata_changes_name_data_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    CardsManagement.update_metadata(
        "Untitled Card",
        "name",
        "World Domination"
    )
    result = json.loads(Config.SETTINGS_PATH.read_text())

    expected_result = helpers.data["updated_bare_config"]
    assert "World Domination" in result["cards"]
    assert expected_result == result


def test_update_metdata_denies_incorrect_card_name_or_field(
            monkeypatch,
            tmp_path
        ):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(KeyError, match="Llama Training"):
        CardsManagement.update_metadata(
            "Llama Training",
            "name",
            "World Domination"
        )

    with pytest.raises(KeyError, match="llamas_collected"):
        CardsManagement.update_metadata(
            "Untitled Card",
            "llamas_collected",
            "World Domination"
        )


def test_update_metadata_denies_restricted_field_change(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(Exception, match="Card field is restricted!"):
        CardsManagement.update_metadata(
            "Untitled Card",
            "id",
            "5d15e4f7-e08e-4f91-9713-fa46f13a9761"
        )


def test_update_metadata_validates_time_as_number(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(
        ValueError,
        match="could not convert string to float: 'Eternal Reign of the Llama'"
    ):
        CardsManagement.update_metadata(
            "Untitled Card",
            "time",
            "Eternal Reign of the Llama"
        )


def test_get_favicon_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "APPDATA_PATH",
        tmp_path
    )
    mock_bytes = MagicMock()
    monkeypatch.setattr(
        CardsManagement,
        "FaviconGrabber",
        helpers.fakeFavicon
    )
    monkeypatch.setattr(
        CardsManagement.Path,
        "write_bytes",
        mock_bytes
    )
    result = CardsManagement.get_favicon("https://youtube.com")
    mock_bytes.assert_called_once_with("https://youtube.com.bytes")
    assert result == Path(tmp_path) / "https:__youtube.com.png"


def test_add_to_site_blocklists_adds_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        CardsManagement,
        "get_favicon",
        lambda x: f"{x}.iconpath"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    CardsManagement.add_to_site_blocklists(
        "Untitled Card",
        "hard_blocked_sites",
        "youtube.com"
    )
    result = json.loads(Config.SETTINGS_PATH.read_text())

    cards_dict = result["cards"]["Untitled Card"]
    assert "youtube.com" in cards_dict["hard_blocked_sites"]
    assert cards_dict["hard_blocked_sites"]["youtube.com"] == {
        "enabled": True,
        "icon_path": "youtube.com.iconpath"
    }


def test_add_to_site_blocklists_denies_malformed_data(monkeypatch, tmp_path):
    cfg = copy.deepcopy(helpers.data["bare_config"])
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="URL not valid!"):
        CardsManagement.add_to_site_blocklists(
            "Untitled Card",
            "hard_blocked_sites",
            "llama"
        )

    cfg["cards"]["Untitled Card"]["soft_blocked_sites"] = {
        "youtube.com": True
    }

    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="'youtube.com' already soft blocked!"):
        CardsManagement.add_to_site_blocklists(
            "Untitled Card",
            "hard_blocked_sites",
            "youtube.com"
        )

    cfg["cards"]["Untitled Card"]["soft_blocked_sites"] = {}
    cfg["cards"]["Untitled Card"]["hard_blocked_sites"] = {
        "youtube.com": True
    }

    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="'youtube.com' already hard blocked!"):
        CardsManagement.add_to_site_blocklists(
            "Untitled Card",
            "soft_blocked_sites",
            "youtube.com"
        )


def test_add_to_site_blocklists_denies_incorrect_card_or_list_name(
            monkeypatch,
            tmp_path
        ):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(KeyError, match="hard_blocked_NIGHTS"):
        CardsManagement.add_to_site_blocklists(
            "Untitled Card",
            "hard_blocked_NIGHTS",
            "https://youtube.com"
        )

    with pytest.raises(KeyError, match="Llama Taming"):
        CardsManagement.add_to_site_blocklists(
            "Llama Taming",
            "hard_blocked_sites",
            "https://youtube.com"
        )


def test_add_to_site_blocklists_denies_restricted_field_change(
            monkeypatch,
            tmp_path
        ):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(Exception, match="Card field is restricted!"):
        CardsManagement.add_to_site_blocklists(
            "Untitled Card",
            "hard_blocked_apps",
            "org.zotero.zotero"
        )


def test_update_site_blocklists_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_blocked_sites"]
    ))

    pretest_dict = helpers.data["bare_config_with_blocked_sites"]
    assert pretest_dict["cards"]["Untitled Card"]["hard_blocked_sites"] == {
        "youtube.com": True,
        "twitter.com": True
    }

    CardsManagement.update_site_blocklists(
        "Untitled Card",
        "hard_blocked_sites",
        {
            "youtube.com": True,
            "twitter.com": False
        }
    )
    result = json.loads(Config.SETTINGS_PATH.read_text())
    cards_dict = result["cards"]["Untitled Card"]

    assert "youtube.com" in cards_dict["hard_blocked_sites"]
    assert "twitter.com" in cards_dict["hard_blocked_sites"]
    assert cards_dict["hard_blocked_sites"]["youtube.com"] is True
    assert cards_dict["hard_blocked_sites"]["twitter.com"] is False
    assert list(cards_dict["hard_blocked_sites"].keys()) == [
        "youtube.com",
        "twitter.com"
    ]


def test_update_site_blocklists_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_blocked_sites"]
    ))

    with pytest.raises(KeyError, match="hard_blocked_NIGHTS"):
        CardsManagement.update_site_blocklists(
            "Untitled Card",
            "hard_blocked_NIGHTS",
            {
                "youtube.com": True,
                "twitter.com": False
            }
        )
    with pytest.raises(Exception, match="Card field is restricted!"):
        CardsManagement.update_site_blocklists(
            "Untitled Card",
            "name",
            {
                "youtube.com": True,
                "twitter.com": False
            }
        )
    with pytest.raises(Exception, match="new_sites_dict is not a dict!"):
        CardsManagement.update_site_blocklists(
            "Untitled Card",
            "hard_blocked_sites",
            "llama"
        )


def test_add_to_app_blocklists_adds_data_darwin(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "APPDATA_PATH",
        Path(tmp_path, "Library", "Application Support", "Lento")
    )
    folders = {
        "application_support": Path(
            "Library",
            "Application Support",
            "Lento"
        ),
        "apps_folder": "Applications",
        "gris_folders": Path("Applications", "GRIS.app", "Contents"),
        "scrivener_folder": Path(
            "Applications",
            "Scrivener.app",
            "Contents"
        ),
        "nnw_folder": Path(
            "Applications",
            "NetNewsWire.app",
            "Contents"
        )
    }
    for f in folders.keys():
        Path(tmp_path, folders[f]).mkdir(parents=True, exist_ok=True)

    for file in ["GRIS", "Scrivener", "NetNewsWire"]:
        plist_file = Path(
            tmp_path,
            "Applications",
            file + ".app",
            "Contents",
            "Info.plist"
        )
        plist_file.write_text(helpers.data[file])

    monkeypatch.setattr(
        Config,
        "MACOS_APPLICATION_FOLDER",
        Path(tmp_path, folders["apps_folder"])
    )
    monkeypatch.setattr(Image, "open", lambda x: helpers.fake_image)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(subprocess, "check_output", helpers.fake_bundle_id)
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    CardsManagement.add_to_app_blocklists(
        "Untitled Card",
        "hard_blocked_apps",
        [
            "/Applications/GRIS.app",
            "/Applications/Scrivener.app",
            "/Applications/NetNewsWire.app"
        ]
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    hb_list = result["cards"]["Untitled Card"]["hard_blocked_apps"]
    assert "GRIS" in hb_list
    assert "Scrivener" in hb_list
    assert "NetNewsWire" in hb_list

    assert hb_list["GRIS"] == {
        "enabled": True,
        "bundle_id": "unity.nomada studio.GRIS",
        "app_icon_path": str(Path(
            Config.APPDATA_PATH,
            "GRIS.jpg"
        ))
    }
    assert hb_list["Scrivener"] == {
        "enabled": True,
        "bundle_id": "com.literatureandlatte.scrivener3",
        "app_icon_path": str(Path(
            Config.APPDATA_PATH,
            "Scrivener.jpg"
        ))
    }
    assert hb_list["NetNewsWire"] == {
        "enabled": True,
        "bundle_id": "com.ranchero.NetNewsWire-Evergreen",
        "app_icon_path": str(Path(
            Config.APPDATA_PATH,
            "NetNewsWire.jpg"
        ))
    }
    assert list(hb_list.keys()) == ["GRIS", "Scrivener", "NetNewsWire"]


def test_add_to_app_blocklists_rejects_dupes_darwin(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )

    cfg = copy.deepcopy(helpers.data["bare_config"])
    cfg["cards"]["Untitled Card"]["soft_blocked_apps"] = {
        "GRIS": {
            "enabled": True,
            "bundle_id": "unity.nomada studio.GRIS",
            "app_icon_path": "~/Library/Application Support/Lento/GRIS.jpg"
        }
    }
    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="'GRIS' already soft blocked!"):
        CardsManagement.add_to_app_blocklists(
            "Untitled Card",
            "hard_blocked_apps",
            [
                "/Applications/GRIS.app",
                "/Applications/Scrivener.app",
                "/Applications/NetNewsWire.app"
            ]
        )

    cfg["cards"]["Untitled Card"]["soft_blocked_apps"] = {}
    cfg["cards"]["Untitled Card"]["hard_blocked_apps"] = {
        "GRIS": {
            "enabled": True,
            "bundle_id": "unity.nomada studio.GRIS",
            "app_icon_path": "~/Library/Application Support/Lento/GRIS.jpg"
        }
    }
    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="'GRIS' already hard blocked!"):
        CardsManagement.add_to_app_blocklists(
            "Untitled Card",
            "soft_blocked_apps",
            [
                "/Applications/GRIS.app",
                "/Applications/Scrivener.app",
                "/Applications/NetNewsWire.app"
            ]
        )


def test_add_to_app_blocklists_adds_data_windows(monkeypatch, tmp_path):
    appdata_dict = copy.deepcopy(helpers.data["proper_apps_dict"])
    appdata_dict["vivaldi"]["path"] = str(Path(
        tmp_path,
        "AppData",
        "Local",
        "Vivaldi",
        "Application",
        "vivaldi.exe"
    ))
    appdata_dict["vivaldi"]["icon_path"] = str(Path(
        tmp_path,
        "AppData",
        "Local",
        "Lento",
        "vivaldi.bmp"
    ))
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    apps_to_add = copy.deepcopy(helpers.data["apps_to_add"])
    apps_to_add[1]["path"] = str(Path(
        tmp_path,
        "AppData",
        "Local",
        "Vivaldi",
        "Application",
        "vivaldi.exe"
    ))
    apps_to_add[1]["icon_path"] = str(Path(
        tmp_path,
        "AppData",
        "Local",
        "Lento",
        "vivaldi.bmp"
    ))

    CardsManagement.add_to_app_blocklists(
        "Untitled Card",
        "hard_blocked_apps",
        apps_to_add
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    hb_list = result["cards"]["Untitled Card"]["hard_blocked_apps"]

    assert "Trello" in hb_list
    assert "vivaldi" in hb_list

    assert hb_list["Trello"] == {
        "enabled": True,
        "path": appdata_dict["Trello"]["path"],
        "app_icon_path": appdata_dict["Trello"]["icon_path"],
    }
    assert hb_list["vivaldi"] == {
        "enabled": True,
        "path": appdata_dict["vivaldi"]["path"],
        "app_icon_path": appdata_dict["vivaldi"]["icon_path"],
    }

    assert list(hb_list.keys()) == ["Trello", "vivaldi"]


def test_add_to_app_blocklists_rejects_dupes_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )

    appdata_dict = helpers.data["proper_apps_dict"]
    cfg = copy.deepcopy(helpers.data["bare_config"])
    cfg["cards"]["Untitled Card"]["soft_blocked_apps"] = {
        "Trello": {
            "enabled": True,
            "path": appdata_dict["Trello"]["path"],
            "app_icon_path": appdata_dict["Trello"]["icon_path"],
        },
    }
    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="'Trello' already soft blocked!"):
        CardsManagement.add_to_app_blocklists(
            "Untitled Card",
            "hard_blocked_apps",
            helpers.data["apps_to_add"]
        )

    cfg["cards"]["Untitled Card"]["soft_blocked_apps"] = {}
    cfg["cards"]["Untitled Card"]["hard_blocked_apps"] = {
        "Trello": {
            "enabled": True,
            "path": appdata_dict["Trello"]["path"],
            "app_icon_path": appdata_dict["Trello"]["icon_path"],
        },
    }
    Config.SETTINGS_PATH.write_text(json.dumps(cfg))

    with pytest.raises(Exception, match="'Trello' already hard blocked!"):
        CardsManagement.add_to_app_blocklists(
            "Untitled Card",
            "soft_blocked_apps",
            helpers.data["apps_to_add"]
        )


def test_update_app_blocklists_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_apps"]
    ))

    CardsManagement.update_app_blocklists(
        "Untitled Card",
        "hard_blocked_apps",
        helpers.data["new_blocklist"]
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())

    new_hblist = result["cards"]["Untitled Card"]["hard_blocked_apps"]
    correct_hblist = helpers.data["bare_config_reordered_apps"]["cards"]["Untitled Card"]["hard_blocked_apps"]  # noqa: E501
    assert new_hblist == correct_hblist
    assert list(new_hblist.keys()) == list(correct_hblist.keys())


def test_update_app_blocklists_rejects_incorrect(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(KeyError, match="Llama"):
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
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "a019868e-f43f-478f-8dcc-ba78c35525c4"
    )

    data = copy.deepcopy(helpers.data["bare_config"])
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["youtube.com"] = True
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["twitter.com"] = True
    data["cards"]["Untitled Card"]["goals"]["Debug USACO problem"] = True
    Config.SETTINGS_PATH.write_text(json.dumps(data))

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

    result = json.loads(Config.SETTINGS_PATH.read_text())
    new_notifs = result["cards"]["Untitled Card"]["notifications"]
    correct_cards = helpers.data["bare_config_with_notif"]["cards"]
    assert new_notifs == correct_cards["Untitled Card"]["notifications"]


def test_add_notification_rejects_incorrect_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "a019868e-f43f-478f-8dcc-ba78c35525c4"
    )

    data = copy.deepcopy(helpers.data["bare_config"])
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["youtube.com"] = True
    data["cards"]["Untitled Card"]["hard_blocked_sites"]["twitter.com"] = True
    data["cards"]["Untitled Card"]["goals"]["Debug USACO problem"] = True
    Config.SETTINGS_PATH.write_text(json.dumps(data))

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
    with pytest.raises(KeyError, match="Llama"):
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
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_multiple_notif"]
    ))

    CardsManagement.update_notification_list(
        "Untitled Card",
        helpers.data["reordered_notifs_dict"]
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    card_notif_dict = result["cards"]["Untitled Card"]["notifications"]
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
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_multiple_notif"]
    ))

    CardsManagement.update_notification_list(
        "Untitled Card",
        helpers.data["deleted_notifs_dict"]
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    card_notif_dict = result["cards"]["Untitled Card"]["notifications"]
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
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

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
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    CardsManagement.add_goal(
        "Untitled Card",
        "Conquer world"
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    new_goals_dict = result["cards"]["Untitled Card"]["goals"]
    assert "Conquer world" in new_goals_dict
    assert new_goals_dict["Conquer world"] is False


def test_add_goal_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(Exception, match="Goal to add is not string!"):
        CardsManagement.add_goal(
            "Untitled Card",
            42
        )
    with pytest.raises(KeyError, match="42"):
        CardsManagement.add_goal(
            42,
            "Conquer world"
        )


def test_update_goal_list_reorders_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_goals"]
    ))

    CardsManagement.update_goal_list(
        "Untitled Card",
        helpers.data["reordered_goal_dict"]
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    card_goals_dict = result["cards"]["Untitled Card"]["goals"]
    assert "Conquer world" in card_goals_dict
    assert "Debug USACO problem" in card_goals_dict
    assert card_goals_dict["Conquer world"] is False
    assert card_goals_dict["Debug USACO problem"] is True


def test_update_goal_list_deletes_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_goals"]
    ))

    CardsManagement.update_goal_list(
        "Untitled Card",
        {"Conquer world": False}
    )

    result = json.loads(Config.SETTINGS_PATH.read_text())
    card_goals_dict = result["cards"]["Untitled Card"]["goals"]
    assert "Conquer world" in card_goals_dict
    assert "Debug USACO problem" not in card_goals_dict
    assert card_goals_dict["Conquer world"] is False
    assert list(card_goals_dict.keys()) == ["Conquer world"]


def test_update_goal_list_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config"]
    ))

    with pytest.raises(Exception, match="new_goals_dict is not a dict!"):
        CardsManagement.update_goal_list(
            "Untitled Card",
            "Llama"
        )
    with pytest.raises(Exception, match="Llama"):
        CardsManagement.update_goal_list(
            "Llama",
            helpers.data["reordered_goal_dict"]
        )


def test_activate_block_in_settings_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )

    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_blocked_sites"]
    ))

    CardsManagement.activate_block_in_settings("Untitled Card")
    result = json.loads(Config.SETTINGS_PATH.read_text())
    expected = helpers.data["bare_config_with_activated_card"]

    assert result == expected
    assert result["activated_card"] == expected["activated_card"]


def test_activate_block_in_settings_rejects_flawed_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )

    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_blocked_sites"]
    ))

    with pytest.raises(Exception, match="Cannot activate nonexistent card!"):
        CardsManagement.activate_block_in_settings("Llama Taming")


def test_deactivate_block_in_settings_works_correctly(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )

    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_activated_card"]
    ))

    CardsManagement.deactivate_block_in_settings()

    result = json.loads(Config.SETTINGS_PATH.read_text())
    expected = helpers.data["bare_config_with_blocked_sites"]
    assert result == expected
    assert result["activated_card"] == expected["activated_card"]
