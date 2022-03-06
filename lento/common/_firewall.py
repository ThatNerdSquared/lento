from abc import ABC, abstractmethod
import json
from lento.config import Config


class Firewall(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    async def block_website(self, website):
        """Will be implemented by children for each platform."""

    @abstractmethod
    async def unblock_websites(self, website):
        """Will be implemented by children for each platform."""

    async def block_hb_websites(self, card_to_activate):
        with open(Config.SETTINGS_PATH, "r", encoding="UTF-8") as userconfig:
            settings = json.load(userconfig)

        websites = settings['cards'][card_to_activate]['hard_blocked_sites']

        for website in websites:
            await self.block_website(str(website))

    async def block_sb_websites(self, card_to_activate):
        with open(Config.SETTINGS_PATH, "r", encoding="UTF-8") as userconfig:
            settings = json.load(userconfig)

        websites = settings['cards'][card_to_activate]['soft_blocked_sites']

        for website in websites:
            await self.block_website(str(website))
