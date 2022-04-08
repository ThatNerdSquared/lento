"""App instance configuration."""
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
    HOME_FOLDER = Path(str(
        os.getenv("USERPROFILE" if platform.system() == "Windows" else "HOME")
    ))
    SETTINGS_PATH = HOME_FOLDER / "lentosettings.json"
    APPDATA_PATH = Path(str(
        HOME_FOLDER / "Library" / "Application Support" if
        platform.system() != "Windows" else HOME_FOLDER / "AppData" / "Local"  # noqa: E501
    )) / "Lento"
    DB_PATH = APPDATA_PATH / "blocktimers.db"
    REVERSED_DOMAIN = "io.github.lentoapp"
    DAEMON_BINARY_PATH = Path(str(
        "/Library/LaunchDaemons/" if platform.system() == "Darwin" else APPDATA_PATH  # noqa: E501
    )) / "lentodaemon"
