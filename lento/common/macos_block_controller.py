import subprocess
from lento.config import Config
from lento.common._block_controller import BlockController


class macOSBlockController(BlockController):
    def __init__(self):
        super().__init__()

    def daemon_launch(self, bundled_binary_path, card_to_use, lasts_for):
        copycmd = " ".join([
            "cp",
            f"\"{bundled_binary_path}\"",
            f"\"{Config.DAEMON_BINARY_PATH}\""
        ])
        daemon_launch_cmd = [
            str(Config.DAEMON_BINARY_PATH),
            str(card_to_use),
            str(lasts_for)
        ]
        results = []
        results.append(subprocess.call(copycmd, shell=True))
        results.append(subprocess.Popen(daemon_launch_cmd, shell=False))
        return results

    def daemon_takedown(self):
        cmd = (f"rm -f \"{Config.DAEMON_BINARY_PATH}\"")
        return subprocess.call(cmd, shell=True)
