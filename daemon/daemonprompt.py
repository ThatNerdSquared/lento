import ctypes
import platform
import subprocess


class DaemonPrompt():
    def __init__(self):
        super().__init__()

    def display_prompt(self, title, message):
        match platform.system():
            case "Darwin":
                return self.macos_softblock_prompt(" ".join([title, message]))
            case "Windows":
                return self.windows_softblock_prompt(title, message)

    def macos_softblock_prompt(self, message):
        choice = subprocess.check_output(" ".join([
            "osascript",
            "-e",
            f"'display dialog \"{message}\"",  # noqa: E501
            "buttons {\"No\", \"Yes\"}'"
        ]), shell=True)
        match choice.decode("utf-8").strip():
            case "button returned:Yes":
                return True
            case "button returned:No":
                return False

    def windows_softblock_prompt(self, title, message):
        choice = ctypes.windll.user32.MessageBoxW(
            0,
            message,
            title,
            36
        )
        # the MessageBox foreign function returns 6 for OK, 7 for No.
        if choice == 6:
            return True
        else:
            return False
