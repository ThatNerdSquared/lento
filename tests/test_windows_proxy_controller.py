import platform
import proxy
import pytest
try:
    import winreg
except ImportError:
    pass
from daemon import get_proxy
from tests import helpers


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="`winreg` cannot be tested on non-Windows platforms"
)
def test_enable_system_proxy_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(winreg, "SetValueEx", helpers.fake_SetValueEx_enable)
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == ["proxyserver_command_run", "proxyenable_command_run"]


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="`winreg` cannot be tested on non-Windows platforms"
)
def test_disable_system_proxy_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(winreg, "SetValueEx", helpers.fake_SetValueEx_disable)
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == ["proxyserver_removed", "proxyenable_disabled"]
