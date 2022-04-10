import platform
from daemon.backends import macos_proxy_controller
from daemon.backends import windows_proxy_controller
from daemon.backends import macos_appblocker
from daemon.backends import windows_appblocker

PROXIES = {
    "Darwin": macos_proxy_controller.macOSProxyController,
    "Windows": windows_proxy_controller.WindowsProxyController
}

APPBLOCKERS = {
    "Darwin": macos_appblocker.macOSAppBlocker,
    "Windows": windows_appblocker.WindowsAppBlocker
}


def get_proxy():
    """Returns the correct Proxy class for each platform."""
    try:
        return PROXIES[platform.system()]()
    except KeyError as e:
        raise KeyError(f'Platform "{platform.system}" not found!') from e


def get_appblocker():
    """Returns the correct AppBlocker class for each platform."""
    try:
        return APPBLOCKERS[platform.system()]()
    except KeyError as e:
        raise KeyError(f'Platform "{platform.system}" not found!') from e
