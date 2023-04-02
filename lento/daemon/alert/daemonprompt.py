import ctypes
import platform
import subprocess


class DaemonPrompt:
    """
    Class handling popup display

    Displays the following types of popup:
    - confirmation prompt: title & message with YES/NO option
    - notif popup: title & message with only YES option
    """

    def display_confirmation_prompt(self, title, message):
        """
        Displays a confirmation style popup prompt with YES/NO options
        """
        match platform.system():
            case "Darwin":
                return self._macos_confirmation_prompt(title, message)
            case "Windows":
                return self._windows_confirmation_prompt(title, message)

    def _macos_confirmation_prompt(self, title, message):
        # call apple script command to launch popup
        choice = subprocess.check_output(
            [
                "osascript",
                "-e",
                f"""display dialog "{message}" with title "{title}" buttons {{"No", "Yes"}}""",  # noqa: E501
            ]
        )

        match choice.decode("utf-8").strip():
            case "button returned:Yes":
                return True
            case "button returned:No":
                return False

        return False

    def _windows_confirmation_prompt(self, title, message):
        MB_YESNO = 0x04
        MB_ICONWARNING = 0x30
        MB_SYSTEMMODAL = 0x1000
        choice = ctypes.windll.user32.MessageBoxW(
            0, message, title, MB_YESNO | MB_ICONWARNING | MB_SYSTEMMODAL
        )
        # the MessageBox foreign function returns 6 for OK, 7 for No.
        if choice == 6:
            return True
        else:
            return False

    def show_notif_popup(self, title, message):
        """
        Display a notification style popup with only YES option
        """
        match platform.system():
            case "Darwin":
                return self.macos_notif_prompt(title, message)
            case "Windows":
                return self.windows_notif_prompt(title, message)

    def macos_notif_prompt(self, title, message):
        # call apple script command to launch popup
        return subprocess.Popen(
            [
                "osascript",
                "-e",
                f"""display dialog "{message}" with title "{title}" buttons "OK" default button 1""",  # noqa: E501
            ]
        )

    def windows_notif_prompt(self, title, message):
        MB_SYSTEMMODAL = 0x1000
        MB_OK = 0x00
        ctypes.windll.user32.MessageBoxW(0, message, title, MB_SYSTEMMODAL | MB_OK)
