from daemon.backends._appblocker import AppBlocker


class macOSAppBlocker(AppBlocker):
    """App blocker using `PyObjC` on macOS."""

    def block_apps(self):
        print("block apps macOS")
