import json
from pathlib import Path
import sys
import proxy
from daemon import get_proxy


def entry(settings_path, card_to_use):
    SETTINGS = json.loads(Path(settings_path).read_text())
    lento_proxy = get_proxy()
    with proxy.Proxy([
        "--port=0",
        "--plugins",
        "daemon.lento_blocker_plugin.LentoBlockerPlugin",
        "--hardblocked-sites",
        lento_proxy.generate_hardblock_list(SETTINGS, card_to_use)
    ]) as lib_proxy:
        lento_proxy.enable_system_proxy(lib_proxy.flags.port)
        proxy.sleep_loop()


if __name__ == '__main__':
    entry(sys.argv[1], sys.argv[2])
