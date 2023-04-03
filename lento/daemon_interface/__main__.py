import json
import logging
import sys

from daemon_interface.daemon_interface import LentoDaemonInterface

from lento.config import Config

if __name__ == "__main__":
    card_to_use = sys.argv[-2]
    time_to_run = sys.argv[-1]

    SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
    task_info = SETTINGS["cards"][card_to_use]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - pid:%(process)d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    interface = LentoDaemonInterface(logging.getLogger())
    interface.start_block_timer(task_info, time_to_run, launch_daemon=True)
