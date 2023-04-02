from lento.daemon.util.util import RepeatTimer
from lento.daemon.alert.lento_notif import LentoNotif
from lento.daemon.alert.daemonprompt import DaemonPrompt

"""
default title & message definitions
"""

APP_DEFAULT_TITLE = "Lento: App Blocked"
WEBSITE_DEFAULT_TITLE = "Lento: Website Blocked"
APP_CONFIRM_DEFAULT_MSG = (
    "You tried to open a blocked app!\nDo you still want to open {}?"  # noqa: E501
)
WEBSITE_CONFIRM_DEFAULT_MSG = (
    "You tried to open a blocked site!\nDo you still want to open {}?"  # noqa: E501
)
APP_INFO_DEFAULT_MSG = "You tried to open {} which is blocked by Lento"
WEBSITE_INFO_DEFAULT_MSG = "You tried to open {} which is blocked by Lento"


class NotifsController:
    """
    Class handling notification and popup display.

    Most methods are class methods since there should
    only be one notification controller handling all
    notification and popup dispatch.
    """

    repeat_notifs = {}

    @classmethod
    def add_repeat_notif(cla, notification_item):
        """
        Adds a repeated notification set to fire
        regularly after an interval

        Parameters:
        notificaiton_item: obj of class NotificationItem
            defined in block_item.py
        """
        # start repeat timer on notification
        interval = notification_item.interval
        timer = RepeatTimer(
            interval, NotifsController._show_banner_notification, [notification_item]
        )
        timer.start()

        # add notification to record
        name = notification_item.name
        cla.repeat_notifs[name] = timer

    @classmethod
    def remove_repeat_notif(cla, name):
        """
        Remove a previously added repeat notification

        Parameters:
        name: name of the notification to remove
        """
        timer = cla.repeat_notifs.get(name)

        if timer:
            timer.cancel()
            cla.repeat_notifs.pop(name)

    @classmethod
    def show_info_popup(cla, title, message, custom_msg=""):
        """
        Displays a popup with title and message and
        only a YES button

        Parameters:
        title: title of popup
        message: message of popup
        """

        if custom_msg is not None and custom_msg != "":
            message = "Lento Says: {}\n\n{}".format(custom_msg, message)

        DaemonPrompt().show_notif_popup(title, message)

    @classmethod
    def show_confirmation_popup(cla, title, message, custom_msg=""):
        """
        Displays a popup with title and message and
        YES & NO Button choices

        Parameters:
        title: title of popup
        message: message of popup

        Returns:
        True if YES is selected, False if NO is selected
        """

        if custom_msg is not None and custom_msg != "":
            message = "Lento Says: {}\n\n{}".format(custom_msg, message)

        return DaemonPrompt().display_confirmation_prompt(title, message)

    @classmethod
    def _show_banner_notification(cla, notification_item):
        """
        Displays a banner notification

        Parameter:
        notificaiton_item: obj of class NotificationItem
            defined in block_item.py
        """
        title = notification_item.title
        message = notification_item.message
        LentoNotif(title, message).send_banner()
