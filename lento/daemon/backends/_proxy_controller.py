from abc import ABC, abstractmethod


class ProxyController(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def enable_system_proxy(self, proxy_port):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def disable_system_proxy(self):
        """Will be implemented by children for each platform."""
