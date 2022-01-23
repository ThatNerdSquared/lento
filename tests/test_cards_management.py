import json
import os
import uuid
import lento.common.cards_management as CardsManagement


def test_create_card_uses_correct_data(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    monkeypatch.setattr(
        uuid.UUID,
        "hex",
        "b0244f7e-8369-49f9-89b4-73811eba3a0e"
    )

    path = os.path.join(os.path.expanduser("~"), "lentosettings.json")

    initial_config = {
        "is_block_running": False,
        "cards": {},
        "application_settings": {
            "theme": "automatic"
        }
    }

    with open(path, "w", encoding="UTF-8") as settings_json:
        settings = json.dump(initial_config, settings_json)

    expected_config = {
        "is_block_running": False,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
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
        },
        "application_settings": {
            "theme": "automatic"
        }
    }

    CardsManagement.create_card()

    with open(path, "r", encoding="UTF-8") as settings_json:
        settings = json.load(settings_json)

    assert settings == expected_config
