import platform
from daemon.backends import macos_proxy_controller
from daemon.backends import windows_proxy_controller

PROXIES = {
    "Darwin": macos_proxy_controller.macOSProxyController,
    "Windows": windows_proxy_controller.WindowsProxyController
}


def get_proxy():
    """Returns the correct Proxy class for each platform."""
    try:
        return PROXIES[platform.system()]()
    except KeyError as e:
        raise KeyError(f'Platform "{platform.system}" not found!') from e
