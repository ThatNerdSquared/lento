from lento.daemon.backends._proxy_controller import ProxyController


class macOSProxyController(ProxyController):
    """Lento proxy controller using `networksetup` on macOS."""

    def enable_system_proxy(self, proxy_port):
        return f"macOS proxy enable endpoint reached at {proxy_port}!"

    def disable_system_proxy(self):
        return "macOS proxy disable endpoint reached!"
