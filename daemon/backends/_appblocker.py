from abc import ABC, abstractmethod


class AppBlocker(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def block_apps(self):
        """Will be implemented by children for each platform."""
