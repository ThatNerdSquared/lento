from abc import ABC, abstractmethod
import lento.common.cards_management as CardsManagement


class BlockController(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def start_daemon(self, card_to_use: str, lasts_for: int):
        """Will be implemented by children for each platform."""

    def start_block(self, card_to_use: str, lasts_for: int) -> None:
        CardsManagement.activate_block_in_settings(card_to_use)
        self.start_daemon(card_to_use, lasts_for)
