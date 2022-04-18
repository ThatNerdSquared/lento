import json
import platform
import subprocess
from pathlib import Path
from lento import utils
from lento.common import get_block_controller
from lento.config import Config
from tests import helpers


def test_start_block_controller_works_properly(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(utils, "get_data_file_path", lambda x: x)
    monkeypatch.setattr(subprocess, "call", helpers.fake_subprocess)
    monkeypatch.setattr(subprocess, "Popen", helpers.fake_subprocess)
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "DAEMON_BINARY_PATH",
        Path("/tmp") / "lentodaemon"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["filled_config"]
    ))
    block_controller = get_block_controller()
    result = block_controller.start_block("Untitled Card", 42)
    assert result == [
        "macOS daemon copied",
        "daemon launched"
    ]


def test_end_block_controller_works_properly(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(utils, "get_data_file_path", lambda x: x)
    monkeypatch.setattr(subprocess, "call", helpers.fake_subprocess)
    monkeypatch.setattr(
        Config,
        "SETTINGS_PATH",
        Path(tmp_path) / "lentosettings.json"
    )
    monkeypatch.setattr(
        Config,
        "DAEMON_BINARY_PATH",
        Path("/tmp") / "lentodaemon"
    )
    Config.SETTINGS_PATH.write_text(json.dumps(
        helpers.data["bare_config_with_activated_card"]
    ))
    block_controller = get_block_controller()
    result = block_controller.end_block()
    assert result == "macOS block cleanup finished"
