import proxy
import logging
import platform
import lento.daemon.lento_blocker_plugin
from lento.daemon.util.util import format_website
from lento.config import Config
from lento.daemon.proxy_controller.macos_proxy_controller import macOSProxyController
from lento.daemon.proxy_controller.windows_proxy_controller import (
    WindowsProxyController,
)  # noqa: E501

PROXIES = {"Darwin": macOSProxyController, "Windows": WindowsProxyController}


class ProxyController:
    """
    Class handling all proxy related functionalities
    """

    def __init__(self, websites_dict):
        self.proxy_server = None
        self.enabled = False

        # parse dictionary of format:
        # { WebsiteBlockItem.website_url : WebsiteBlockItem }
        # to a list of [WebsiteBlockItem.website_url, ...] according to
        # softblock/hardblock
        self.hardblocked_websites = self._parse_websites(websites_dict)
        self.softblocked_websites = self._parse_websites(websites_dict, softblock=True)

    def enable_system_proxy(self, proxy_port):
        """
        Enables system proxy according to platform
        """
        if not self.enabled:
            PROXIES[platform.system()]().enable_system_proxy(proxy_port)
            self.enabled = True

    def disable_system_proxy(self):
        """
        Disables system proxy according to platform
        """
        if self.enabled:
            PROXIES[platform.system()]().disable_system_proxy()
            self.enabled = False

    def setup(self, task_name, num_acceptors):
        """
        Starts a proxy server. Proxy server processes should be running
        at the end of the method call.

        Parameters
        task_name: the name of the TimerTask that the proxy belongs to
        num_acceptors: number of acceptors to launch the proxy with
        """

        logging.info(
            f"Initializing proxy server with \
                     {num_acceptors} acceptor(s)"
        )

        # make proxy log also part of daemon logs
        logging.info("Hello")
        log_file_path = str(Config.APPDATA_PATH) + "/lentodaemon_proxy.log"
        logging.info("logging proxy to: {}".format(log_file_path))

        self.proxy_server = proxy.Proxy(
            [
                "--port=0",
                "--num-acceptors",
                str(num_acceptors),
                "--plugins",
                "daemon.lento_blocker_plugin.LentoBlockerPlugin",
                "--hardblocked-sites",
                self.hardblocked_websites,
                "--softblocked-sites",
                self.softblocked_websites,
                "--task-name",
                task_name,
                "--log-file",
                log_file_path,
            ]
        )

        logging.info("Setting up proxy server")
        self.proxy_server.setup()

        proxy_port = self.proxy_server.flags.port

        logging.info(
            f"Enabling system proxy for proxy \
                     server at port {proxy_port}"
        )
        self.enable_system_proxy(proxy_port)

    def cleanup(self):
        """
        Terminates the proxy server process and disables
        system proxy
        """
        self.disable_system_proxy()
        logging.info("Shutting down proxy server")
        self.proxy_server.shutdown()

    def _parse_websites(self, websites_dict, softblock=False):
        """
        Converts a dictionary of form
            { WebsiteBlockItem.website_url : WebsiteBlockItem }
        to a list of [WebsiteBlockItem.website_url, ...]
        """
        website_list = []

        for website in websites_dict:
            website_item = websites_dict.get(website)
            if website_item.is_soft_block == softblock:
                # websites are formatted to xxxx.com, without "www."
                # for example: www.google.com -> google.com
                website_url = format_website(website_item.website_url)
                website_list.append(website_url)

        return website_list
