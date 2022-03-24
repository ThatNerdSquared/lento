import proxy
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

    def init_proxy(self):
        with proxy.Proxy([
            "--port=0",
            "--plugins",
            "proxy.plugin.FilterByUpstreamHostPlugin",
            "--filtered-upstream-hosts",
            "slack.com,www.slack.com",
        ]) as lib_proxy:
            proxy.sleep_loop()
            result = self.enable_system_proxy(lib_proxy.flags.port)
            return result
