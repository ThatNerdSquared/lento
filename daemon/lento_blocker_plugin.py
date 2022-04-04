import datetime
from typing import Optional
from proxy.http import httpStatusCodes
from proxy.common.flag import flags
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from proxy.http.exception import HttpRequestRejected
from daemon import get_proxy
from daemon.db import DBController


class LentoBlockerPlugin(HttpProxyBasePlugin):
    """
    Drop or redirect outgoing traffic:
    - If request is to host in hard-blocked list, drop.
    - If request is to host in soft-blocked list, redirect to custom webserver.
    """

    flags.add_argument(
        "--hardblocked-sites",
        type=str,
        help="List of domains to hard-block, seperated by commas.",
    )
    flags.add_argument(
        "--softblocked-sites",
        type=str,
        help="List of domains to soft-block, seperated by commas.",
    )

    def before_upstream_connection(
        self, request: HttpParser
    ) -> Optional[HttpParser]:

        hb_websites = self.flags.hardblocked_sites.split(",")
        sb_websites = self.flags.softblocked_sites.split(",")

        # there's a small possibility a request won't have a host for some
        # reason but this is mostly here to appease the Python type checker
        if request.host:
            host = request.host.decode("UTF-8")
            if host in hb_websites:
                # Block the site immediately if it's in the hard-blocked list.
                raise HttpRequestRejected(
                    status_code=httpStatusCodes.I_AM_A_TEAPOT,
                    reason=b"I\'m a tea pot",
                )
            # TODO: refactor the below because it is super messy.
            if host in sb_websites:
                # Start a series of checks if the site is soft-blocked.
                print(f"====SOFTBLOCKED SITE DETECTED: {host}====")
                db = DBController()
                allowed = db.check_if_site_allowed(host)
                if not allowed:
                    data = db.get_site_entry(host)
                    if data is None:
                        # Prompt the user if there's no existing record for the
                        # site in the DB.
                        lento_proxy = get_proxy()
                        choice = lento_proxy.softblock_prompt(host)
                        if not choice:
                            # Block the site if the user chooses No, and update
                            # this in the DB for future connections to the site
                            db.update_site(host, False)
                            raise HttpRequestRejected(
                                status_code=httpStatusCodes.I_AM_A_TEAPOT,
                                reason=b"I\'m a tea pot",
                            )
                        else:
                            # Allow the site to pass through if the user
                            # chooses Yes, and update this in the DB
                            db.update_site(host, True)
                    else:
                        if (
                            datetime.datetime.now() - data["last_asked"]
                        ).total_seconds() < 10:
                            # some sites send multiple requests to the host on
                            # load, so this prevents spamming prompts.
                            raise HttpRequestRejected(
                                status_code=httpStatusCodes.I_AM_A_TEAPOT,
                                reason=b"I\'m a tea pot",
                            )
                        else:
                            # Prompt the user if the site isn't allowed and
                            # it's been 10+ seconds since the last prompt.
                            lento_proxy = get_proxy()
                            choice = lento_proxy.softblock_prompt(host)
                            if not choice:
                                db.update_site(host, False)
                                raise HttpRequestRejected(
                                    status_code=httpStatusCodes.I_AM_A_TEAPOT,
                                    reason=b"I\'m a tea pot",
                                )
                            else:
                                db.update_site(host, True)
        return request
