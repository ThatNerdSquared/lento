import copy
import os
import platform
import subprocess
from lento import utils
from tests import helpers


def test_remove_dupes_blanks_and_whitespace():
    test_list = ["llamas   ", "are", "cool", "", "cool", "llamas", ""]
    new_list = utils.remove_dupes_blanks_and_whitespace(test_list)

    assert new_list == ["llamas", "are", "cool"]


def test_get_apps_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(subprocess, "getoutput", helpers.fake_subprocess)
    monkeypatch.setattr(subprocess, "call", lambda x, shell="": "")

    apps = utils.get_apps()

    proper_apps_dict = copy.deepcopy(helpers.data["proper_apps_dict"])
    proper_apps_dict["vivaldi"]["path"] = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "Vivaldi",
        "Application",
        "vivaldi.exe"
    )
    proper_apps_dict["vivaldi"]["icon_path"] = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "Lento",
        "vivaldi.bmp"
    )

    assert apps == proper_apps_dict
