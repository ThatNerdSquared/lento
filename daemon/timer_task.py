import logging
from daemon.block_item import AppBlockItem, WebsiteBlockItem
from daemon.block_item import NotificationItem
from daemon.util.util import RepeatTimer, format_website
from daemon.util.db import DBController
from daemon.alert.notifications_controller import NotifsController
from daemon.app_blocker.appblocker import AppBlocker
from daemon.proxy_controller.proxy_controller import ProxyController
from datetime import datetime, timedelta


class TimerTask:
    """
    Class that handles a timer block task
    Each TimerTask object should be corresopnding to an
    instance of a "Card" being activated in GUI
    """

    def __init__(self, info_dict=None, completion_handler=None):
        """
        Parameters
        info_dict: dictionary containing task info, this includes
            the apps & websites blocked in the task and the repeat
            notifications to be displayed. The info dictionary
            should follow the same format as a "card" in
            lentosettings.json
        completion_handler: a method called when the TimerTask
            completes
        """

        self.init()
        self.completion_handler = completion_handler

        if info_dict:
            self.name = info_dict.get("name")
            self.task_interval = int(info_dict.get("duration"))

            # extract the blocked websites, blocked apps, and
            # notifications from the dictionary
            self._extract_blocked_websites(info_dict)
            self._extract_blocked_apps(info_dict)
            self._extract_notifications(info_dict)

    def init(self):
        """
        Initializes the properties of the class
        """
        self.app_blocker = None
        self.proxy = None
        self.name = None
        self.task_interval = 0
        self.end_time = None

        # dictionary is of the form {WebsiteBlockItem.procname
        # : WebsiteBlockItem}
        self.blocked_websites = {}
        # dictionary is of the form {AppBlockItem.procname : AppBlockItem}
        self.blocked_apps = {}
        # list of the form [NotificationItem, ...]
        self.notifications = []
        self.main_timer = RepeatTimer(1, self.time_check, [])
        self.completion_handler = None

    def start(self, num_acceptors):
        """
        Start the TimerTask, launch app & website blocking
        and repeated notifications

        Parameters
        num_acceptors: number of acceptors (processes) for
            proxy server
        """
        # if the end time is not set, set the task end time
        # when the task starts
        if not self.end_time:
            self.end_time = datetime.now() + \
                timedelta(seconds=self.task_interval)

        # initialize app blocker and proxy
        self.app_blocker = AppBlocker(self.blocked_apps)
        self.proxy = ProxyController(self.blocked_websites)
        self.proxy.setup(self.name, num_acceptors)

        # start main timer
        logging.info("Starting main timer")
        self.main_timer.start()

        # adding repeating notifications
        for notifcation_item in self.notifications:
            NotifsController.add_repeat_notif(notifcation_item)

        # save the timer task to database
        DBController.save_timer_task(self)

        logging.info("Task started")

    def cleanup(self):
        """
        Cleans up the TimerTask
        """
        logging.info("Cleaning up daemon and quit")
        self.proxy.cleanup()
        logging.info("Cancelling main timer")
        self.main_timer.cancel()

        # remove the task from database
        DBController.remove_timer_task(self.name)

    def is_complete(self):
        """
        Returns if the task is complete
        """
        return datetime.now() > self.end_time

    def time_check(self):
        """
        Method repeated every 1 second to check
        if TimerTask is complete and to trigger
        app blocking
        """
        if self.is_complete():
            self.cleanup()
            if self.completion_handler:
                self.completion_handler()

            return

        self.app_blocker.check_and_block_apps()

    def print(self):
        logging.info("***********Timer Task: {}***********".format(self.name))
        logging.info("Task Interval: {}s".format(self.task_interval))
        logging.info("End Date: {}".format(self.end_time))
        logging.info("***********Blocked Websites***********")
        for website in self.blocked_websites:
            website_item = self.blocked_websites.get(website)
            website_item.print()
        logging.info("***********Blocked Apps***********")
        for app in self.blocked_apps:
            app_item = self.blocked_apps.get(app)
            app_item.print()
        logging.info("***********Notifications***********")
        for notification_item in self.notifications:
            notification_item.print()
        logging.info("**********************************************")

    def _extract_blocked_websites(self, info_dict):
        """
        Construct the blocked_website dictionary from the info
        dictionary
        """

        # python nested function
        def extract_items(info_dict, key, is_soft_block):
            sites_dict = info_dict.get(key)
            if not sites_dict:
                return

            for website in sites_dict.keys():
                website_info = sites_dict[website]
                if website_info["enabled"]:
                    # format website to take out "www."
                    website = format_website(website)
                    website_item = WebsiteBlockItem(
                        website,
                        self.name,
                        soft_block=is_soft_block
                    )
                    allow_interval = website_info["allow_interval"]
                    website_item.allow_interval = allow_interval
                    website_item.popup_msg = website_info["popup_msg"]
                    self.blocked_websites[website] = website_item

        extract_items(info_dict, "hard_blocked_sites", False)
        extract_items(info_dict, "soft_blocked_sites", True)

    def _extract_blocked_apps(self, info_dict):
        """
        Construct the blocked_app dicitonary from the info
        dictionary
        """

        # python nested function
        def extract_items(info_dict, key, is_soft_block):
            apps_dict = info_dict.get(key)
            if not apps_dict:
                return

            for app in apps_dict.keys():
                app_info = apps_dict[app]
                if app_info["enabled"]:
                    app_item = AppBlockItem(
                        app,
                        self.name,
                        soft_block=is_soft_block
                    )
                    app_item.allow_interval = app_info["allow_interval"]
                    app_item.popup_msg = app_info["popup_msg"]
                    self.blocked_apps[app] = app_item

        extract_items(info_dict, "hard_blocked_apps", False)
        extract_items(info_dict, "soft_blocked_apps", True)

    def _extract_notifications(self, info_dict):
        """
        Construct the notifications list from the info dictionary
        """

        notifications = info_dict.get("notifications")
        if not notifications:
            return

        for notif_id in notifications:
            notification_info = notifications[notif_id]
            if notification_info["enabled"]:
                interval = notification_info["time_interval_trigger"]
                title = notification_info["title"]
                message = notification_info["body"]
                notif_item = NotificationItem(
                    notif_id,
                    title,
                    message,
                    interval,
                    self.name
                )

                self.notifications.append(notif_item)
