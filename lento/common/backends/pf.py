from lento.common.backends._firewall import Firewall


class PacketFilter(Firewall):
    def block_website(self, website):
        print(f"{website} now being blocked by pf")
