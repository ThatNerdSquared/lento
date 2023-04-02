import os
import platform
import subprocess
import sys
from urllib.parse import urlparse
from pathlib import Path
from lento.config import Config

"""
Utility Methods
"""


def get_data_file_path(relative_path):
    """
    Returns the absolute path of an asset based on
    relative path
    """
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")

    return os.path.join(base, relative_path)


def is_url(url):
    """
    Check if the input string is a URL
    """
    scheme_included = False
    schemes_to_check = ["https://", "http://", "file://", "ftp://"]
    for scheme in schemes_to_check:
        if len(scheme) <= len(url) and url[: len(scheme)] == scheme:
            scheme_included = True

    if not scheme_included:
        url = "https://" + url

    result = urlparse(url)
    if "." not in result.netloc:
        return False

    return True


def get_apps():
    current_os = platform.system()
    apps = {}
    if current_os == "Windows":
        command = 'powershell "Get-Process -FileVersionInfo -ErrorAction SilentlyContinue | Select-Object FileName"'  # noqa: E501
        raw_data = subprocess.getoutput(command).split("\n")
        items = remove_dupes_blanks_and_whitespace(raw_data[3:])
        for app_path in items:
            app_name = os.path.basename(app_path).replace(".exe", "")
            if (
                os.path.join(Config.DRIVE_LETTER, "Program Files", "WindowsApps")
                in app_path
            ):
                command = f'powershell "(Get-AppxPackage -Name "*{app_name}*" | Get-AppxPackageManifest).package.applications.application.VisualElements.DefaultTile.Square310x310Logo"'  # noqa: E501
                app_icon = subprocess.getoutput(command)
                if app_icon == "":
                    app_icon_path = None
                else:
                    app_icon_path = os.path.join(
                        Config.DRIVE_LETTER,
                        "Program Files",
                        "WindowsApps",
                        Path(app_path).parts[3],
                        "".join([app_icon[:-4], ".scale-200.png"]),
                    )
            else:
                app_icon_path = os.path.join(
                    os.path.expanduser("~"),
                    "AppData",
                    "Local",
                    "Lento",
                    f"{app_name}.bmp",
                )
                if not os.path.exists(app_icon_path):
                    command = f"powershell \"Add-Type -AssemblyName System.Drawing; [System.Drawing.Icon]::ExtractAssociatedIcon('{app_path}').toBitmap().Save('{app_icon_path}')\""  # noqa: E501
                    subprocess.call(command, shell=True)
            apps[app_name] = {"path": app_path, "icon_path": app_icon_path}
    elif current_os == "Darwin":
        raise Exception("This function does not currently support macOS.")
    else:
        raise Exception("Something went wrong and the OS name could not be found.")

    return apps


def remove_dupes_blanks_and_whitespace(list_to_process):
    no_blanks_list = list(filter(None, list_to_process))
    no_extra_whitespace_list = []
    for item in no_blanks_list:
        no_extra_whitespace_list.append(item.rstrip())
    no_dupes_list = list(dict.fromkeys(no_extra_whitespace_list))

    return no_dupes_list
