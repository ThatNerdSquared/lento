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
        launch = " ".join([
            f"\"{str(Config.DAEMON_BINARY_PATH)}\"",
            f"\"{card_to_use}\"",
            str(lasts_for)
        ])
        commands = [
            f"powershell \"cp '{bundled_binary_path}' '{Config.DAEMON_BINARY_PATH}'\"",  # noqa: E501
            f"powershell \"{launch}\""
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result

    def daemon_takedown(self):
        cmd = f"powershell \"rm -Force '{Config.DAEMON_BINARY_PATH}'\""
        return subprocess.call(cmd, shell=True)
