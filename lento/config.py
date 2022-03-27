"""App instance configuration."""
from PySide6.QtCore import QStandardPaths
import dotenv
import os
import sys
import platform
from pathlib import Path


def get_data_file_path(relative_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath('.')

    return os.path.join(base, relative_path)


dotenv.load_dotenv(dotenv_path=get_data_file_path('.env'), override=True)  # noqa: E501


class Config:
    TEST_VAR = os.getenv('TEST_VAR')
    MACOS_APPLICATION_FOLDER = Path("/Applications/")
    DRIVE_LETTER = "C:\\"
    SETTINGS_PATH = Path(str(
        os.getenv("USERPROFILE" if platform.system() == "Windows" else "HOME")
    )) / "lentosettings.json"
    PF_ANCHOR_PATH = Path("/etc/pf.anchors/io.github.lento")
    PF_CONFIG_PATH = Path("/etc/pf.conf")
    APPDATA_PATH = Path(
        QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) if platform.system() != "Windows" else Path(os.getenv("USERPROFILE")) / "AppData" / "Local"
    ) / "Lento"
    DB_PATH = APPDATA_PATH / "blocktimers.db"
