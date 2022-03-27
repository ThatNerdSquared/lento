import ctypes
import subprocess
from daemon.backends._proxy_controller import ProxyController


class WindowsProxyController(ProxyController):
    """Lento proxy controller using Powershell on Windows."""

    def __init__(self):
        super().__init__()

    def softblock_prompt(self, site):
        choice = ctypes.windll.user32.MessageBoxW(
            None,
            f"Do you still want to access {site}, or are you getting distracted?",
            "You tried to access a soft-blocked site!",
            0
        )
        print(choice)
        return False

    def enable_system_proxy(self, proxy_port):
        reg = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"  # noqa: E501
        commands = [
            f"powershell 'Set-ItemProperty -Path {reg} ProxyEnable -value 1'",
            f"powershell 'Set-ItemProperty -Path {reg} ProxyServer -value \"localhost:{proxy_port}\"'",  # noqa: E501
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result

    def disable_system_proxy(self):
        reg = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"  # noqa: E501
        commands = [
            f"powershell 'Set-ItemProperty -Path {reg} ProxyEnable -value 0'",
            f"powershell 'Remove-ItemProperty -Path {reg} ProxyServer'",
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result
