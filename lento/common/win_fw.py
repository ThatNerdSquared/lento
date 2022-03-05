from lento.common._firewall import Firewall


class WindowsFirewall(Firewall):
    def block_website(self, website):
        print(f"{website} now being blocked by winfirewall")
