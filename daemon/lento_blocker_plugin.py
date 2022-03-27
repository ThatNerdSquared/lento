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

        if request.host:
            host = request.host.decode("UTF-8")
            if host in hb_websites:
                raise HttpRequestRejected(
                    status_code=httpStatusCodes.I_AM_A_TEAPOT,
                    reason=b"I\'m a tea pot",
                )
            if host in sb_websites:
                print(f"====SOFTBLOCKED SITE DETCTED:  {host}====")
                db = DBController()
                is_blocked = db.check_if_site_blocked(host)
                if is_blocked:
                    raise HttpRequestRejected(
                        status_code=httpStatusCodes.I_AM_A_TEAPOT,
                        reason=b"I\'m a tea pot",
                    )
                else:
                    data = db.get_site_entry(host)
                    if (
                        datetime.datetime.now() - data.last_asked
                    ).total_seconds() < 10:
                        raise HttpRequestRejected(
                            status_code=httpStatusCodes.I_AM_A_TEAPOT,
                            reason=b"I\'m a tea pot",
                        )
                    else:
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
