from pathlib import Path
import socket
from lento.common._firewall import Firewall
from lento.config import Config


class PacketFilter(Firewall):
    """Firewall on macOS."""
    async def block_website(self, website):
        """pf requires certain syntax in an anchor file to block sites."""

        if not Path(Config.PF_ANCHOR_PATH).exists():
            with open(Config.PF_ANCHOR_PATH, "w", encoding="UTF-8") as anchor:
                anchor.write("""# Options
set block-policy drop
set fingerprints "/etc/pf.os"
set ruleset-optimization basic
set skip on lo0

#
# Rules for Lento blocks
#""")

        with open(Config.PF_ANCHOR_PATH, "r", encoding="UTF-8") as anchor:
            pf_anchor = anchor.read()

        site = socket.gethostbyname(website)
        anchor_text = f"""block return out proto tcp from any to {site}
block return out proto udp from any to {site}"""

        with open(Config.PF_ANCHOR_PATH, "w", encoding="UTF-8") as anchor:
            anchor.write(f"""{pf_anchor}\n{anchor_text}""")

    async def unblock_websites(self):
        with open(Config.PF_ANCHOR_PATH, "w", encoding="UTF-8") as anchor:
            anchor.write('')
