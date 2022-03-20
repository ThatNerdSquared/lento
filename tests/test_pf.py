import os
import json
import socket
import sys
import pytest
from pathlib import Path
from lento.config import Config
from lento.daemon import get_firewall
from tests import helpers

pytest_plugins = ('pytest_asyncio')


@pytest.mark.asyncio
async def test_pf_block_hardblocked_websites(monkeypatch, tmp_path):
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

    assert helpers.data["expected_pf_anchor"] == result_pf_anchor


@pytest.mark.asyncio
async def test_pf_block_softblocked_websites(monkeypatch, tmp_path):
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
        json.dump(helpers.data["bare_config_with_sb_sites"], config)

    fw = get_firewall()
    await fw.block_sb_websites('Untitled Card')

    with open(Config.PF_ANCHOR_PATH, "r", encoding="UTF-8") as anchor:
        result_pf_anchor = anchor.read()

    assert helpers.data["expected_pf_anchor"] == result_pf_anchor


@pytest.mark.asyncio
async def test_pf_unblock_hardblocked_websites(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "PF_ANCHOR_PATH",
        Path(tmp_path) / "io.github.lento"
    )
    monkeypatch.setattr(sys, "platform", "darwin")

    with open(Config.PF_ANCHOR_PATH, "w", encoding="UTF-8") as anchor:
        anchor.write(helpers.data["expected_pf_anchor"])

    fw = get_firewall()
    await fw.unblock_websites()

    with open(Config.PF_ANCHOR_PATH, "r", encoding="UTF-8") as anchor:
        result_pf_anchor = anchor.read()

    assert result_pf_anchor == ''
