import os
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
