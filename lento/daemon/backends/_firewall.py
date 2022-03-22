from abc import ABC, abstractmethod
import json
import subprocess
from lento.config import Config


class Firewall(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def pre_block(self):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def hardblock_website(self, website):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def softblock_website(self, website):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def unblock_websites(self, website):
        """Will be implemented by children for each platform."""

    def block_websites(self, card_to_activate):
        self.pre_block()
        settings = json.loads(Config.SETTINGS_PATH.read_text())

        sb_websites = settings['cards'][card_to_activate]['soft_blocked_sites']
        hb_websites = settings['cards'][card_to_activate]['hard_blocked_sites']

        for website in sb_websites:
            self.softblock_website(str(website))
        for website in hb_websites:
            self.hardblock_website(str(website))
        subprocess.call("/sbin/pfctl -E -f /etc/pf.conf", shell=True)
