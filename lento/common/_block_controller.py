from abc import ABC, abstractmethod


class BlockController(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def start_daemon(self, card_to_use: str, lasts_for: int):
        """Will be implemented by children for each platform."""
