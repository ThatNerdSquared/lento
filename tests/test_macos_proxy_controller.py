import proxy
import platform
from lento.daemon import get_proxy


def test_enable_system_proxy_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == "macOS proxy enable endpoint reached at 42!"
