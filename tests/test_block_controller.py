import json
import subprocess
from pathlib import Path
from lento import utils
from lento.common.block_controller import BlockController
from lento.config import Config
from tests import helpers


def test_block_controller_works_properly(monkeypatch, tmp_path):
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
        helpers.data["filled_config"]
    ))
    block_controller = BlockController()
    result = block_controller.start_block("Untitled Card", 42)
    assert result == [
        "daemon copied",
        "daemon launched"
    ]
