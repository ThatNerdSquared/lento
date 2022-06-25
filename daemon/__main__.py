import json
import multiprocessing
import os
import signal
import sys
import threading
import proxy
from daemon import get_proxy
from daemon.appblocker import AppBlocker
from daemon.db import DBController
from daemon.lento_blocker_plugin import LentoBlockerPlugin  # noqa: F401
from daemon.notifications_controller import NotifsController
from lento.config import Config


def entry(card_to_use, lasts_for):
    SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
    lento_proxy = get_proxy()
    db = DBController()
    db.clear_db()
    db.create_main_timer(lasts_for)

    app_blocker = AppBlocker()
    hb_apps = app_blocker.generate_hardblocked_apps_list(card_to_use)
    sb_apps = app_blocker.generate_softblocked_apps_list(card_to_use)

    notifs_controller = NotifsController()
    notifs_controller.clear_notifs()
    notifs_dict = SETTINGS["cards"][card_to_use]["notifications"]
    for item in notifs_dict.keys():
        if not notifs_dict[item]["enabled"]:
            del notifs_dict[item]
    notifs_controller.set_up_notifs(notifs_dict)

    time_check(os.getpid(), hb_apps, sb_apps)

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


def time_check(MASTER_PID, hb_apps, sb_apps):
    db = DBController()
    notifs_controller = NotifsController()
    is_block_over = db.check_if_block_is_over()
    if not is_block_over:
        app_blocker = AppBlocker()
        app_blocker.block_apps(hb_apps, sb_apps)
        triggered_notifs = notifs_controller.check_for_time_triggers()
        if triggered_notifs:
            notifs_controller.fire_notifs(triggered_notifs)
        threading.Timer(1, time_check, [MASTER_PID, hb_apps, sb_apps]).start()
    else:
        lento_proxy = get_proxy()
        lento_proxy.disable_system_proxy()
        db.clear_db()
        notifs_controller.clear_notifs()
        # needed to kill the whole daemon process, not just this child thread
        os.kill(MASTER_PID, signal.SIGTERM)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # name of card to use, time to run session in seconds
    entry(sys.argv[-2], sys.argv[-1])
