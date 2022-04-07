from daemon.backends._appblocker import AppBlocker


class WindowsAppBlocker(AppBlocker):
    """App blocker on Windows."""

    def block_apps(self):
        print("block apps Windows")
