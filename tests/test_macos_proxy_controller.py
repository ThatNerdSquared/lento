import proxy
import platform
from lento.daemon import get_proxy


def test_enable_system_proxy_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", "Darwin")
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    lib_proxy = get_proxy()
    result = lib_proxy.init_proxy()
    assert result.startswith("macOS proxy enable endpoint reached at ") is True
