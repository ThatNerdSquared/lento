from tests import helpers
import proxy
import platform
import winreg
from daemon import get_proxy


def test_enable_system_proxy_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(winreg, "SetValueEx", helpers.fake_SetValueEx_enable)
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == ["proxyserver_command_run", "proxyenable_command_run"]


def test_disable_system_proxy_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(winreg, "SetValueEx", helpers.fake_SetValueEx_disable)
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == ["proxyserver_removed", "proxyenable_disabled"]
