from abc import ABC, abstractmethod


class ProxyController(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def softblock_prompt(self, site):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def enable_system_proxy(self, proxy_port):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def disable_system_proxy(self):
        """Will be implemented by children for each platform."""

    def generate_hardblock_list(self, SETTINGS, card_to_use):
        raw_hb_websites = SETTINGS["cards"][card_to_use]["hard_blocked_sites"]
        hb_websites = []
        for item in raw_hb_websites.keys():
            if raw_hb_websites[item]:
                hb_websites.append(item)
                hb_websites.append("www." + item)

        return ",".join(hb_websites)

    def generate_softblock_list(self, SETTINGS, card_to_use):
        raw_sb_websites = SETTINGS["cards"][card_to_use]["soft_blocked_sites"]
        sb_websites = []
        for item in raw_sb_websites.keys():
            if raw_sb_websites[item]:
                sb_websites.append(item)
                sb_websites.append("www." + item)

        return ",".join(sb_websites)
