import json
import psutil
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
            for softblocked_app in sb_apps:
                if softblocked_app in procname:
                    print(
                        f"===SOFTBLOCKED APP DETECTED: {softblocked_app}==="
                    )
                    proc.terminate()

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
