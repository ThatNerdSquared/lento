import platform
from lento.common.macos_block_controller import macOSBlockController
from lento.common.windows_block_controller import WindowsBlockController


BLOCK_CONTROLLERS = {
    "Darwin": macOSBlockController,
    "Windows": WindowsBlockController,
}


def get_block_controller():
    """Returns the correct BlockController for each platform."""
    try:
        return BLOCK_CONTROLLERS[platform.system()]()
    except KeyError as e:
        raise KeyError(f"Platform '{platform.system}' not found!") from e