import json
import os
import platform
import subprocess
import sys
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
        command = "powershell \"Get-StartApps | convertto-json\""
        app_data = json.loads(subprocess.getoutput(command))
        for app in app_data:
            apps[app['Name']] = app['AppID']
    elif current_os == "Darwin":
        raise Exception("This function does not currently support macOS.")
    else:
        raise Exception(
            "Something went wrong and the OS name could not be found."
        )

    return(apps)
