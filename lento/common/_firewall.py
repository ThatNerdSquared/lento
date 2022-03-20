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
    def block_website(self, website):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def unblock_websites(self, website):
        """Will be implemented by children for each platform."""

    def block_hb_websites(self, card_to_activate):
        self.pre_block()
        with open(Config.SETTINGS_PATH, "r", encoding="UTF-8") as userconfig:
            settings = json.load(userconfig)

        websites = settings['cards'][card_to_activate]['hard_blocked_sites']

        for website in websites:
            self.block_website(str(website))
        subprocess.call("/sbin/pfctl -E -f /etc/pf.conf", shell=True)

    def block_sb_websites(self, card_to_activate):
        self.pre_block()
        with open(Config.SETTINGS_PATH, "r", encoding="UTF-8") as userconfig:
            settings = json.load(userconfig)

        websites = settings['cards'][card_to_activate]['soft_blocked_sites']

        for website in websites:
            self.block_website(str(website))
        subprocess.call("/sbin/pfctl -E -f /etc/pf.conf", shell=True)
