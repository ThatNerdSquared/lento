import json
import os
import platform
import subprocess
import sys
import uuid
from urllib.parse import urlparse


def get_data_file_path(relative_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath('.')

    return os.path.join(base, relative_path)


def is_url(url):
    scheme_included = False
    schemes_to_check = ["https://", "http://", "file://", "ftp://"]
    for scheme in schemes_to_check:
        if len(scheme) <= len(url) and url[:len(scheme)] == scheme:
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
        subprocess.call("powershell \"Add-Type -AssemblyName System.Drawing\"")
        command = "powershell \"Get-Process -FileVersionInfo -ErrorAction SilentlyContinue | Select-Object FileName\""  # noqa: E501
        raw_data = subprocess.getoutput(command).split("\n")
        items = remove_dupes_blanks_and_whitespace(raw_data[3:])
        for app_path in items:
            app_name = os.path.basename(app_path).replace(".exe", "")
            if "C:\\Program Files\\WindowsApps" in app_path:
                command = f"powershell \"(Get-AppxPackage -Name \"*{app_name}*\" | Get-AppxPackageManifest).package.applications.application.VisualElements.DefaultTile.Square310x310Logo\""  # noqa: E501
                app_icon = subprocess.getoutput(command)
                if app_icon == "":
                    app_icon_path = None
                else:
                    app_icon_path = os.path.join(
                        app_path[:app_path.rindex("\\")+1],
                        "".join([
                            app_icon[:-4],
                            ".scale-200.png"
                        ])
                    )
            else:
                app_icon_path = os.path.join(
                    os.path.expanduser("~"),
                    "AppData",
                    "Local",
                    "Lento",
                    f"{app_name}.bmp"
                )
                command = f"powershell \"[System.Drawing.Icon]::ExtractAssociatedIcon(\'{app_path}\').toBitmap().Save({app_icon_path})\""  # noqa: E501
            apps[app_name] = {
                "path": app_path,
                "icon_path": app_icon_path
            }
    elif current_os == "Darwin":
        raise Exception("This function does not currently support macOS.")
    else:
        raise Exception(
            "Something went wrong and the OS name could not be found."
        )

    return(apps)


def remove_dupes_blanks_and_whitespace(list_to_process):
    no_blanks_list = list(filter(None, list_to_process))
    no_extra_whitespace_list = []
    for item in no_blanks_list:
        no_extra_whitespace_list.append(item.rstrip())
    no_dupes_list = list(dict.fromkeys(no_extra_whitespace_list))

    return no_dupes_list
