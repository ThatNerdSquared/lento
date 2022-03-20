import os
import json
import socket
import subprocess
import sys
from pathlib import Path
from lento.config import Config
from lento.daemon import get_firewall
from tests import helpers


def test_pf_block_hardblocked_websites(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "PF_ANCHOR_PATH",
        Path(tmp_path) / "io.github.lento"
    )
    monkeypatch.setattr(Config, "PF_CONFIG_PATH", Path(tmp_path) / "pf.conf")
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(socket, "gethostbyname", helpers.fake_gethost)
    monkeypatch.setattr(subprocess, "call", helpers.fake_subprocess)
    Config.SETTINGS_PATH.write_text(
        json.dumps(helpers.data["bare_config_with_blocked_sites"])
    )

    fw = get_firewall()
    fw.block_hb_websites('Untitled Card')

    result_pf_anchor = Config.PF_ANCHOR_PATH.read_text()
    result_pf_conf = Config.PF_CONFIG_PATH.read_text()
    print(result_pf_anchor)
    print(helpers.data["expected_pf_anchor"])

    assert helpers.data["expected_pf_anchor"] == result_pf_anchor
    assert helpers.data["expected_pf_conf"] == result_pf_conf


def test_pf_block_softblocked_websites(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "PF_ANCHOR_PATH",
        Path(tmp_path) / "io.github.lento"
    )
    monkeypatch.setattr(Config, "PF_CONFIG_PATH", Path(tmp_path) / "pf.conf")
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(socket, "gethostbyname", helpers.fake_gethost)
    monkeypatch.setattr(subprocess, "call", helpers.fake_subprocess)
    Config.SETTINGS_PATH.write_text(
        json.dumps(helpers.data["bare_config_with_sb_sites"])
    )

    fw = get_firewall()
    fw.block_sb_websites('Untitled Card')

    result_pf_anchor = Config.PF_ANCHOR_PATH.read_text()
    result_pf_conf = Config.PF_CONFIG_PATH.read_text()

    assert helpers.data["expected_pf_anchor"] == result_pf_anchor
    assert helpers.data["expected_pf_conf"] == result_pf_conf


def test_pf_unblock_websites(monkeypatch, tmp_path):
    monkeypatch.setattr(
        Config,
        "PF_ANCHOR_PATH",
        Path(tmp_path) / "io.github.lento"
    )
    monkeypatch.setattr(Config, "PF_CONFIG_PATH", Path(tmp_path) / "pf.conf")
    monkeypatch.setattr(sys, "platform", "darwin")

    Config.PF_ANCHOR_PATH.write_text(helpers.data["expected_pf_anchor"])
    Config.PF_CONFIG_PATH.write_text(helpers.data["expected_pf_conf"])

    fw = get_firewall()
    fw.unblock_websites()

    result_pf_anchor = Config.PF_ANCHOR_PATH.read_text()
    result_pf_conf = Config.PF_CONFIG_PATH.read_text()

    assert result_pf_anchor == ""
    assert result_pf_conf == ""
