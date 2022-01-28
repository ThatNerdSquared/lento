import copy
import json
import os
import pytest
import uuid
import lento.common.cards_management as CardsManagement
from tests import helpers


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


def test_update_site_blocklists_correctly_adds_data(monkeypatch, tmp_path):
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
