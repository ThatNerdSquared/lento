import subprocess
import proxy
import platform
from daemon import get_proxy
from tests import helpers


def test_enable_system_proxy_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(proxy, "sleep_loop", lambda: "proxy started")
    monkeypatch.setattr(subprocess, "call", helpers.fake_subprocess)
    lento_proxy = get_proxy()
    result = lento_proxy.enable_system_proxy(42)
    assert result == [
        "macOS web proxy activated",
        "macOS secure web proxy activated"
    ]
