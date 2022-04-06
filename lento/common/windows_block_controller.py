from lento.common._block_controller import BlockController


class WindowsBlockController(BlockController):
    """Lento block controller using Powershell on Windows."""

    def __init__(self):
        super().__init__()

    def start_daemon(self, card_to_use: str, lasts_for: int):
        return print(
            f"Windows daemon started with args: {card_to_use}, {lasts_for}"
        )
