from lento.common._block_controller import BlockController


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
        return ("Windows daemon started with args:"
                f"{bundled_binary_path}, {card_to_use}, {lasts_for}")

    def daemon_takedown(self):
        return "Windows daemon taken down"
