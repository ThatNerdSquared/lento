from abc import ABC, abstractmethod
from typing import Iterable


class Firewall(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def block_website(self, website):
        """Will be implemented by children for each platform."""

    def block_websites(self, websites: Iterable | str):
        for website in websites:
            self.block_website(website)
