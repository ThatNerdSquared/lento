import logging
from datetime import datetime
from typing import Optional

from proxy.common.flag import flags
from proxy.http import httpStatusCodes
from proxy.http.exception import HttpRequestRejected
from proxy.http.parser import HttpParser
from proxy.http.proxy import HttpProxyBasePlugin

from lento.daemon.alert.notifications_controller import (
    WEBSITE_CONFIRM_DEFAULT_MSG,
    WEBSITE_DEFAULT_TITLE,
    WEBSITE_INFO_DEFAULT_MSG,
    NotifsController,
)
from lento.daemon.util.db import DBController
from lento.daemon.util.util import format_website

# interval to not show a hardblock popup once a
# hardblock popup is shown. From testing, observe
# that multiple CONNECT request to the same URL maybe
# captured by the plugin within a short interval
POPUP_INTERVAL = 60


class LentoBlockerPlugin(HttpProxyBasePlugin):
    """
    Drop or redirect outgoing traffic:
    - If request is to host in hard-blocked list, drop.
    - If request is to host in soft-blocked list, redirect to custom webserver.
    """

    flags.add_argument(
        "--hardblocked-sites",
        type=list,
        help="List of domains to hard-block",
    )
    flags.add_argument(
        "--softblocked-sites",
        type=list,
        help="List of domains to soft-block",
    )

    flags.add_argument(
        "--task-name",
        type=str,
        help="Name of the timer block task",
    )

    def __init__(
        self,
        uid,
        flags,
        client,
        event_queue,
        upstream_conn_pool,
    ) -> None:
        self.uid = uid  # pragma: no cover
        self.flags = flags  # pragma: no cover
        self.client = client  # pragma: no cover
        self.event_queue = event_queue  # pragma: no cover
        self.upstream_conn_pool = upstream_conn_pool
        DBController.init()

    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        """
        Called just before Proxy upstream connection is established

        Note on browsers with "Preloading" enabled, popups may appear
        when user is searching for things on the search bar
        (this happens for Safari)
        """
        global POPUP_INTERVAL

        # load the list of hard blocked and soft blocked websites
        hb_websites = self.flags.hardblocked_sites
        sb_websites = self.flags.softblocked_sites
        task_name = self.flags.task_name

        # there's a small possibility a request won't have a host for some
        # reason but this is mostly here to appease the Python type checker
        if request.host:
            # format the host URL from "www.google.com" to "google.com"
            host = request.host.decode("UTF-8")
            host = format_website(host)

            # if URL is hard blcked, show popup and block site
            if host in hb_websites:
                logging.info(f"====HARDBLOCKED SITE DETECTED: {host}====")
                web_item = DBController.get_website_item(task_name, host)

                # because multiple web requests may be sent for the
                # same page load, show hard blocked popup every
                # 60 seconds
                if (
                    datetime.now() - web_item.last_asked
                ).total_seconds() > POPUP_INTERVAL:
                    NotifsController.show_info_popup(
                        WEBSITE_DEFAULT_TITLE,
                        WEBSITE_INFO_DEFAULT_MSG.format(host),
                        custom_msg=web_item.popup_msg,
                    )

                    # update the database with the time
                    # that the popup is shown
                    DBController.update_website_record(
                        web_item.owner, web_item.website_url, datetime.now(), False
                    )

                raise HttpRequestRejected(
                    status_code=httpStatusCodes.I_AM_A_TEAPOT,
                    reason=b"I'm a tea pot",
                )

            # start a series of checks if the site is soft-blocked.
            elif host in sb_websites:
                # assume the website is allowed
                is_allowed = True

                # load the corresponding WebsiteBlockItem from database,
                # need information from the object to determine if to
                # show popup or not
                web_item = DBController.get_website_item(task_name, host)

                # show the popup if we are past the allow interval
                if (
                    datetime.now() - web_item.last_asked
                ).total_seconds() > web_item.allow_interval:
                    logging.info(f"====SOFTBLOCKED SITE DETECTED: {host}====")

                    is_allowed = NotifsController.show_confirmation_popup(
                        WEBSITE_DEFAULT_TITLE,
                        WEBSITE_CONFIRM_DEFAULT_MSG.format(host),
                        custom_msg=web_item.popup_msg,
                    )

                    # update the last asked time and is_allowed for
                    # the WebsiteBlockItem object
                    DBController.update_website_record(
                        web_item.owner, web_item.website_url, datetime.now(), is_allowed
                    )

                # block the website if current time is within allow
                # interval and the website is not allowed
                else:
                    if not web_item.is_allowed:
                        is_allowed = False

                if not is_allowed:
                    raise HttpRequestRejected(
                        status_code=httpStatusCodes.I_AM_A_TEAPOT,
                        reason=b"I'm a tea pot",
                    )

        return request
