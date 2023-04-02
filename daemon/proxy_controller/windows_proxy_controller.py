try:
    import winreg
except ImportError:
    pass


class WindowsProxyController:
    """Lento proxy controller using Powershell on Windows."""

    def __init__(self):
        super().__init__()
        self.MAIN_REG_PATH = (
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"  # noqa: E501
        )

    def set_registry_key(self, key, value, type):
        # Open the key so that we can modify it
        REGISTRY_SETTINGS = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, self.MAIN_REG_PATH, 0, winreg.KEY_ALL_ACCESS
        )
        return winreg.SetValueEx(REGISTRY_SETTINGS, key, 0, type, value)

    def enable_system_proxy(self, proxy_port):
        value = f"http://localhost:{proxy_port}"
        server_command = self.set_registry_key("ProxyServer", value, winreg.REG_SZ)
        enable_command = self.set_registry_key("ProxyEnable", 1, winreg.REG_DWORD)
        return [server_command, enable_command]

    def disable_system_proxy(self):
        server_command = self.set_registry_key("ProxyServer", "", winreg.REG_SZ)
        enable_command = self.set_registry_key("ProxyEnable", 0, winreg.REG_DWORD)
        return [server_command, enable_command]
