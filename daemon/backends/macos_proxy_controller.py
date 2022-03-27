import subprocess
from daemon.backends._proxy_controller import ProxyController


class macOSProxyController(ProxyController):
    """Lento proxy controller using `networksetup` on macOS."""

    def __init__(self):
        super().__init__()

    def softblock_prompt(self, site):
        choice = subprocess.check_output(" ".join([
            "osascript",
            "-e",
            f"'display dialog \"You tried to access a soft-blocked site! Do you still want to access {site}, or are you getting distracted?\"",  # noqa: E501
            "buttons {\"No\", \"Yes\"}'"
        ]), shell=True)
        match choice.decode("utf-8").strip():
            case "button returned:Yes":
                return True
            case "button returned:No":
                return False

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
