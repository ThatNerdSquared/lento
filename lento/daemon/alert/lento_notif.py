import platform
import subprocess
from plyer import notification


class LentoNotif:
    """
    Class handling banner notification display
    """

    def __init__(self, title, body, audio_paths=None):
        """
        Parameters:
        title: title string of the notification
        body: body string of the notification
        audio_path: audio file to play when notif is sent
        """
        super().__init__()
        self.title = title
        self.body = body
        # TODO: add support for audio
        self.audio_paths = audio_paths

    def send_banner(self):
        match platform.system():
            case "Darwin":
                return self._macos_notif()
            case "Windows":
                return self._windows_notif()

    def _macos_notif(self):
        subprocess.Popen(
            [
                "osascript",
                "-e",
                f"""display notification "{self.body}" with title "{self.title}\"""",  # noqa: E501
            ]
        )

    def _windows_notif(self):
        print(f"==\nWIN NOTIF WITH TITLE {self.title} AND BODY {self.body}\n==")
        notification.notify(
            title=self.title, message=self.body, app_name="Lento", timeout=10
        )
