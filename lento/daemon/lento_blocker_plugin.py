from typing import Optional
from proxy.http import httpStatusCodes
from proxy.common.flag import flags
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from proxy.http.exception import HttpRequestRejected


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

    def before_upstream_connection(
        self, request: HttpParser
    ) -> Optional[HttpParser]:

        hb_websites = self.flags.hardblocked_sites.split(",")

        if request.host:
            if bytes.decode(bytes(request.host)) in hb_websites:
                raise HttpRequestRejected(
                    status_code=httpStatusCodes.I_AM_A_TEAPOT,
                    reason=b"I\'m a tea pot",
                )
        return request
