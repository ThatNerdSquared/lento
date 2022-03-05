import os
import json
import sys
from lento.config import Config
from lento.common.backends import get_firewall
from tests import helpers


def test_block_websites(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        os.path.join(tmp_path, "lentosettings.json")
    )
    monkeypatch.setattr(sys, "platform", "darwin")
    with open(Config.SETTINGS_PATH, "w", encoding="UTF-8") as config:
        json.dump(helpers.data["bare_config"], config)

    fw = get_firewall()
    fw.block_websites(["google.com"])

    with open(Config.SETTINGS_PATH, "r", encoding="UTF-8") as config:
        settings = json.load(config)

    # assert settings == 
