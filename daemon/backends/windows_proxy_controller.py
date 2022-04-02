import ctypes
import subprocess
import winreg
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
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyServer')
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyEnable')
        INTERNET_SETTINGS = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        )
        print(INTERNET_SETTINGS)
        reg_type_server = winreg.QueryValueEx(INTERNET_SETTINGS, "ProxyServer")
        reg_type_enable = winreg.QueryValueEx(INTERNET_SETTINGS, "ProxyEnable")
        value = f"http://localhost:{proxy_port}"
        winreg.SetValueEx(
            INTERNET_SETTINGS,
            "ProxyServer",
            0,
            reg_type_server[1],
            value
        )
        winreg.SetValueEx(
            INTERNET_SETTINGS,
            "ProxyEnable",
            0,
            reg_type_enable[1],
            1
        )

    def disable_system_proxy(self):
        INTERNET_SETTINGS = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        )
        reg_type_enable = winreg.QueryValueEx(INTERNET_SETTINGS, "ProxyEnable")
        winreg.DeleteValue(
            INTERNET_SETTINGS,
            "ProxyServer",
        )
        winreg.SetValueEx(
            INTERNET_SETTINGS,
            "ProxyEnable",
            0,
            reg_type_enable[1],
            0
        )
