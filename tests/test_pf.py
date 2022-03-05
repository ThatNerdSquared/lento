import copy
import os
import json
import socket
import sys
import pytest
from pathlib import Path
from lento.config import Config
from lento.common import get_firewall
from tests import helpers

pytest_plugins = ('pytest_asyncio')


@pytest.mark.asyncio
async def test_block_websites(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        os.path.join(tmp_path, "lentosettings.json")
    )
    monkeypatch.setattr(
        Config,
        "PF_ANCHOR_PATH",
        Path(tmp_path) / "io.github.lento"
    )
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(socket, "gethostbyname", helpers.fake_gethost)
    with open(Config.SETTINGS_PATH, "w", encoding="UTF-8") as config:
        json.dump(helpers.data["bare_config_with_blocked_sites"], config)

    fw = get_firewall()
    await fw.block_hb_websites('Untitled Card')

    with open(Config.PF_ANCHOR_PATH, "r", encoding="UTF-8") as anchor:
        result_pf_anchor = anchor.read()

    expected_pf_anchor = """# Options
set block-policy drop
set fingerprints "/etc/pf.os"
set ruleset-optimization basic
set skip on lo0

#
# Rules for Lento blocks
#
block return out proto tcp from any to 172.217.14.206
block return out proto tcp from any to 104.244.42.193"""

    assert expected_pf_anchor == result_pf_anchor
