import logging
import plistlib
from abc import ABC, abstractmethod
from pathlib import Path


class _AbstractAppInfo(ABC):
    # @abstractmethod
    # def show_app_picker(self):
    #     """Will be implemented by children."""

    @abstractmethod
    def get_bundle_id(self, app_path):
        """Will be implemented by children."""

    @abstractmethod
    def get_icon_path(self, app_path):
        """Will be implemented by children."""


class DarwinAppInfo(_AbstractAppInfo):
    def __init__(self):
        super().__init__()

    def get_bundle_id(self, app_path):
        plist_path = Path(app_path, "Contents", "Info.plist")
        logging.info(f"Loading app info from plist path: {plist_path}")
        raw_plist = plistlib.load(plist_path)
        bundle_id = raw_plist.get("CFBundleIdentifier")
        return bundle_id

    def get_icon_path(self, app_path):
        plist_path = Path(app_path, "Contents", "Info.plist")
        logging.info(f"Loading app info from plist path: {plist_path}")
        raw_plist = plistlib.load(plist_path)
        icon_filename = raw_plist.get("CFBundleIconFile")
        icon_path = Path(self.app_path, "Contents", "Resources", icon_filename)
        logging.info(f"App icon found: {icon_path}")
        return icon_path


class WindowsAppInfo(_AbstractAppInfo):
    def __init__(self):
        super().__init__()
