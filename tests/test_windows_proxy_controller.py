import proxy
import platform
from lento.daemon import get_proxy


def test_enable_system_proxy_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == "Windows proxy enable endpoint reached at 42!"
