import ctypes
import winreg
from daemon.backends._proxy_controller import ProxyController


class WindowsProxyController(ProxyController):
    """Lento proxy controller using Powershell on Windows."""

    def __init__(self):
        super().__init__()
        self.MAIN_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"  # noqa: E501

    def softblock_prompt(self, site):
        choice = ctypes.windll.user32.MessageBoxW(
            0,
            f"Do you still want to access {site}, or are you getting distracted?",  # noqa: E501
            "You tried to access a soft-blocked site!",
            36
        )
        # the MessageBox foreign function returns 6 for OK, 7 for No.
        if choice == 6:
            return True
        else:
            return False

    def set_registry_key(self, key, value, type):
        # Open the key so that we can modify it
        REGISTRY_SETTINGS = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            self.MAIN_REG_PATH,
            0,
            winreg.KEY_ALL_ACCESS
        )
        return winreg.SetValueEx(REGISTRY_SETTINGS, key, 0, type, value)

    def enable_system_proxy(self, proxy_port):
        value = f"http://localhost:{proxy_port}"
        server_command = self.set_registry_key(
            "ProxyServer",
            value,
            winreg.REG_SZ
        )
        enable_command = self.set_registry_key(
            "ProxyEnable",
            1,
            winreg.REG_DWORD
        )
        return [server_command, enable_command]

    def disable_system_proxy(self):
        server_command = self.set_registry_key(
            "ProxyServer",
            "",
            winreg.REG_SZ
        )
        enable_command = self.set_registry_key(
            "ProxyEnable",
            0,
            winreg.REG_DWORD
        )
        return [server_command, enable_command]
