import datetime
import json
import psutil
import subprocess
from daemon.daemonprompt import DaemonPrompt
from daemon.db import DBController
from daemon.notifications_controller import NotifsController
from lento.config import Config


class AppBlocker():
    def __init__(self):
        super().__init__()

    def block_apps(self, hb_apps, sb_apps):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                procname = proc.name()
            except psutil.NoSuchProcess:
                continue
            except psutil.ZombieProcess:
                continue
            for hardblocked_app in hb_apps:
                if hardblocked_app in procname:
                    print(
                        f"===HARDBLOCKED APP DETECTED: {hardblocked_app}==="
                    )
                    proc.terminate()
                    notifs_controller = NotifsController()
                    triggered_notifs = notifs_controller.get_triggered_notifs(
                        hardblocked_app
                    )
                    if triggered_notifs:
                        notifs_controller.fire_notifs(triggered_notifs)
            for softblocked_app in sb_apps:
                if softblocked_app in procname:
                    print(
                        f"===SOFTBLOCKED APP DETECTED: {softblocked_app}==="
                    )
                    notifs_controller = NotifsController()
                    triggered_notifs = notifs_controller.get_triggered_notifs(
                        softblocked_app
                    )
                    if triggered_notifs:
                        notifs_controller.fire_notifs(triggered_notifs)
                    # TODO: refactor the below, it's not unbearable but there's
                    # probably a better way to do this.
                    db = DBController()
                    record = db.get_app_record(procname)
                    PROCESS_BINARY = proc.exe()
                    if record is None:
                        proc.terminate()
                        prompt = DaemonPrompt()
                        choice = prompt.display_prompt(
                            "You tried to open a soft-blocked app!",
                            f"Do you still want to open {procname}, or are you getting distracted?",  # noqa: E501
                        )
                        if choice:
                            db.update_app_record(procname, True)
                            subprocess.Popen(PROCESS_BINARY)
                        else:
                            db.update_app_record(procname, False)
                    else:
                        if not record["is_allowed"]:
                            proc.terminate()
                            if (
                                datetime.datetime.now() - record["last_asked"]
                            ).total_seconds() > 10:
                                prompt = DaemonPrompt()
                                choice = prompt.display_prompt(
                                    "You tried to open a soft-blocked app!",
                                    f"Do you still want to open {procname}, or are you getting distracted?",  # noqa: E501
                                )
                                if choice:
                                    db.update_app_record(procname, True)
                                    subprocess.Popen(PROCESS_BINARY)
                                else:
                                    db.update_app_record(procname, False)

    def generate_hardblocked_apps_list(self, card_to_use):
        SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
        raw_hb_apps = SETTINGS["cards"][card_to_use]["hard_blocked_apps"]
        hb_apps = []
        for item in raw_hb_apps.keys():
            if raw_hb_apps[item]["enabled"]:
                hb_apps.append(item)
        return hb_apps

    def generate_softblocked_apps_list(self, card_to_use):
        SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
        raw_sb_apps = SETTINGS["cards"][card_to_use]["soft_blocked_apps"]
        sb_apps = []
        for item in raw_sb_apps.keys():
            if raw_sb_apps[item]["enabled"]:
                sb_apps.append(item)
        return sb_apps
