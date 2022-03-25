from daemon.backends._proxy_controller import ProxyController


class WindowsProxyController(ProxyController):
    """Lento proxy controller using Powershell on Windows."""

    def enable_system_proxy(self, proxy_port):
        return f"Windows proxy enable endpoint reached at {proxy_port}!"

    def disable_system_proxy(self):
        return "Windows proxy disable endpoint reached!"
