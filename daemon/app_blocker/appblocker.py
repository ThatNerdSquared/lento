import psutil
import subprocess
import logging
from daemon.alert.notifications_controller import (
    NotifsController,
    APP_DEFAULT_TITLE,
)  # noqa: E501
from daemon.alert.notifications_controller import (
    APP_INFO_DEFAULT_MSG,
    APP_CONFIRM_DEFAULT_MSG,
)  # noqa: E501
from daemon.util.db import DBController
from datetime import datetime


class AppBlocker:
    """
    Class handling app blocking logic
    """

    def __init__(self, blocked_apps_dict):
        """
        Parameters
        blocked_apps_dict: dictionary of AppBlockItem of the
            form {AppBlockItem.procanme : AppBlockItem}. This
            is for quick lookup of the process name when
            checking if a process should be blocked
        """
        super().__init__()
        self.blocked_app_dict = blocked_apps_dict

    def check_and_block_apps(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                procname = proc.name()
            except psutil.NoSuchProcess:
                continue
            except psutil.ZombieProcess:
                continue

            if procname in self.blocked_app_dict:
                app_item = self.blocked_app_dict.get(procname)

                # check if the process is in set of hardblocked
                # apps. If yes, show popup and terminate it.
                if not app_item.is_soft_block:
                    logging.info(f"===HARDBLOCKED APP DETECTED: {procname}===")
                    NotifsController.show_info_popup(
                        APP_DEFAULT_TITLE,
                        APP_INFO_DEFAULT_MSG.format(procname),
                        custom_msg=app_item.popup_msg,
                    )
                    self._terminate_process(proc)

                # If the process is softblocked, start a series
                # of checks
                else:
                    # get the process binary path right now
                    # otherwise if process is terminated,
                    # proc.exe() will return None
                    try:
                        PROCESS_BINARY = proc.exe()
                    except (psutil.NoSuchProcess, psutil.ZombieProcess):
                        continue

                    # if current time is past the allow interval,
                    # display popup and ask user if this app should
                    # be allow
                    if (
                        datetime.now() - app_item.last_asked
                    ).total_seconds() > app_item.allow_interval:
                        logging.info(f"===SOFTBLOCKED APP DETECTED: {procname}===")

                        # terminate the app first, don't want the
                        # app to be useable while waiting for user
                        # response to popup
                        self._terminate_process(proc)

                        is_allowed = NotifsController.show_confirmation_popup(
                            APP_DEFAULT_TITLE,
                            APP_CONFIRM_DEFAULT_MSG.format(procname),
                            custom_msg=app_item.popup_msg,
                        )

                        if is_allowed:
                            subprocess.Popen(PROCESS_BINARY)

                        # update the AppBlockItem object and
                        # the database
                        app_item.last_asked = datetime.now()
                        app_item.is_allowed = is_allowed

                        DBController.update_app_record(
                            app_item.owner,
                            app_item.procname,
                            datetime.now(),
                            is_allowed,
                        )

                    # if current time is still within the allow interval,
                    # check if the app was allowed by the user during
                    # this current interval
                    else:
                        if not app_item.is_allowed:
                            logging.info(f"===SOFTBLOCKED APP DETECTED: {procname}===")
                            if self._terminate_process(proc):
                                NotifsController.show_info_popup(
                                    APP_DEFAULT_TITLE,
                                    APP_INFO_DEFAULT_MSG.format(procname),
                                    custom_msg=app_item.popup_msg,
                                )

    def _generate_apps_dict(self, blocked_apps_dict, softblock=False):
        """
        Convert a list of AppBlockItem objects into dictionaries of the
        form { AppBlockItem.procname : AppBlockItem }
        """
        app_dict = dict()
        for procname in blocked_apps_dict:
            app_item = blocked_apps_dict.get(procname)
            if app_item.is_soft_block == softblock:
                app_dict[app_item.procname] = app_item

        return app_dict

    def _terminate_process(self, proc):
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False

        return True
