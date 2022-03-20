import sys
from lento.daemon.backends import pf
from lento.daemon.backends import win_fw

FIREWALLS = {
    'darwin': pf.PacketFilter,
    'windows': win_fw.WindowsFirewall
}


def get_firewall():
    """Returns the correct Firewall class for the platform."""
    try:
        return FIREWALLS[sys.platform]()
    except KeyError as e:
        raise KeyError(f'Platform "{sys.platform}" not found!') from e
