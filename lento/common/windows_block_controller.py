import subprocess
from lento.common._block_controller import BlockController
from lento.config import Config


class WindowsBlockController(BlockController):
    """Lento block controller using Powershell on Windows."""

    def __init__(self):
        super().__init__()

    def daemon_launch(
        self,
        bundled_binary_path,
        card_to_use: str,
        lasts_for: int
    ):
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
        results.append(
            subprocess.call(f"powershell \"{copycmd}\"", shell=True)
        )
        results.append(subprocess.Popen(daemon_launch_cmd, shell=False))
        return results

    def daemon_takedown(self):
        cmd = f"powershell \"rm -Force '{Config.DAEMON_BINARY_PATH}'\""
        return subprocess.call(cmd, shell=True)
