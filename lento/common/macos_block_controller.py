import subprocess
from lento.config import Config
from lento.common._block_controller import BlockController


class macOSBlockController(BlockController):
    def __init__(self):
        super().__init__()

    def daemon_launch(self, bundled_binary_path, card_to_use, lasts_for):
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

    def daemon_takedown(self):
        cmd = ("osascript -e 'do shell script"
               f" \"rm \\\"{Config.DAEMON_BINARY_PATH}\\\""
               "\" with administrator privileges'")
        return subprocess.call(cmd, shell=True)