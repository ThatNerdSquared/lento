import json
import os
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


