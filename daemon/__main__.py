import json
import multiprocessing
import os
import signal
import sys
import threading
import proxy
from daemon import get_proxy
from daemon.db import DBController
from daemon.lento_blocker_plugin import LentoBlockerPlugin  # noqa: F401
from lento.config import Config


def entry(card_to_use, lasts_for):
    SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
    lento_proxy = get_proxy()
    db = DBController()
    db.clear_db()
    db.create_main_timer(lasts_for)
    time_check(os.getpid())
    with proxy.Proxy([
        "--port=0",
        "--plugins",
        "daemon.lento_blocker_plugin.LentoBlockerPlugin",
        "--hardblocked-sites",
        lento_proxy.generate_hardblock_list(SETTINGS, card_to_use),
        "--softblocked-sites",
        lento_proxy.generate_softblock_list(SETTINGS, card_to_use),
    ]) as lib_proxy:
        lento_proxy.enable_system_proxy(lib_proxy.flags.port)
        proxy.sleep_loop()


def time_check(MASTER_PID):
    db = DBController()
    is_block_over = db.check_if_block_is_over()
    if not is_block_over:
        threading.Timer(1, time_check, [MASTER_PID]).start()
    else:
        lento_proxy = get_proxy()
        lento_proxy.disable_system_proxy()
        db.clear_db()
        # needed to kill the whole daemon process, not just this child thread
        os.kill(MASTER_PID, signal.SIGTERM)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # name of card to use, time to run session in seconds
    entry(sys.argv[1], sys.argv[2])
