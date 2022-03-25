import subprocess
from daemon.backends._proxy_controller import ProxyController


class macOSProxyController(ProxyController):
    """Lento proxy controller using `networksetup` on macOS."""

    def enable_system_proxy(self, proxy_port):
        commands = [
            f"networksetup -setwebproxy wi-fi localhost {proxy_port}",
            f"networksetup -setsecurewebproxy wi-fi localhost {proxy_port}"
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result

    def disable_system_proxy(self):
        commands = [
            "networksetup -setwebproxystate wi-fi off",
            "networksetup -setsecurewebproxystate wi-fi off"
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result
