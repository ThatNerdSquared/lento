import os
import platform
import subprocess
from lento.config import Config
from lento import utils
from tests import helpers


def test_remove_dupes_blanks_and_whitespace():
    test_list = ["llamas   ", "are", "cool", "", "cool", "llamas", ""]
    new_list = utils.remove_dupes_blanks_and_whitespace(test_list)

    assert new_list == ["llamas", "are", "cool"]


def test_get_apps_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(os.path, "expanduser", lambda x: tmp_path)
    if platform.system() == "Darwin":
        monkeypatch.setattr(Config, "DRIVE_LETTER", "C:/")
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(subprocess, "getoutput", helpers.fake_subprocess)
    monkeypatch.setattr(subprocess, "call", lambda x, shell="": "")

    apps = utils.get_apps()

    assert apps == {
        "Trello": {
            "path": str(os.path.join(
                Config.DRIVE_LETTER,
                "Program Files",
                "WindowsApps",
                "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
                "app",
                "Trello.exe"
            )),
            "icon_path": str(os.path.join(
                Config.DRIVE_LETTER,
                "Program Files",
                "WindowsApps",
                "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
                "assets",
                "Square310x310Logo.scale-200.png"
            ))
        },
        "vivaldi": {
            "path": os.path.join(
                os.path.expanduser("~"),
                "AppData",
                "Local",
                "Vivaldi",
                "Application",
                "vivaldi.exe"
            ),
            "icon_path": os.path.join(
                os.path.expanduser("~"),
                "AppData",
                "Local",
                "Lento",
                "vivaldi.bmp"
            )
        }
    }
