import subprocess
from lento import utils
import lento.common.cards_management as CardsManagement
from lento.config import Config


class BlockController():
    def __init__(self):
        super().__init__()

    def start_block(self, card_to_use: str, lasts_for: int):
        CardsManagement.activate_block_in_settings(card_to_use)
        bundled_binary_path = utils.get_data_file_path("lentodaemon")
        commands = [
            ("osascript -e 'do shell script"
                f" \"cp \\\"{bundled_binary_path}\\\""
                f" \\\"{Config.DAEMON_BINARY_PATH}\\\"\""
                " with administrator privileges'"),
            " ".join([
                f"\"{str(Config.DAEMON_BINARY_PATH)}\"",
                f"\"{card_to_use}\"",
                str(lasts_for)
            ])
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result
