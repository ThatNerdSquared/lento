import platform
import playsound
import subprocess
from pathlib import Path
from plyer import notification
from daemon.daemonprompt import DaemonPrompt


class LentoNotif():
    def __init__(self, notif):
        super().__init__()
        self.name = notif["name"]
        self.title = notif["title"]
        self.body = notif["body"]
        self.audio_paths = notif["audio_paths"]

    def send_banner(self):
        match platform.system():
            case "Darwin":
                return self.macos_notif()
            case "Windows":
                return self.windows_notif()

    def macos_notif(self):
        subprocess.Popen([
            "osascript",
            "-e",
            f"""display notification "{self.body}" with title "{self.title}\""""  # noqa: E501
        ])

    def windows_notif(self):
        print(
            f"==\nWIN NOTIF WITH TITLE {self.title} AND BODY {self.body}\n=="
        )
        notification.notify(
            title=self.title,
            message=self.body,
            app_name="Lento",
            timeout=10
        )

    def play_audio(self):
        match platform.system():
            case "Darwin":
                for item in self.audio_paths.keys():
                    subprocess.call(["afplay", Path(self.audio_paths[item])])
            case "Windows":
                for item in self.audio_paths.keys():
                    playsound.playsound(Path(self.audio_paths[item]))

    def show_notif_popup(self):
        prompt = DaemonPrompt()
        return prompt.show_notif_popup(self.title, self.body)
