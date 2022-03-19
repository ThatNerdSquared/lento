import elevate
import os
from pathlib import Path
import socket
from lento import utils
from lento.common._firewall import Firewall
from lento.config import Config


class PacketFilter(Firewall):
    """Firewall on macOS."""

    async def pre_block(self):
        # utils.escalate_privileges()
        elevate.elevate()
        with open(Config.PF_CONFIG_PATH, "a", encoding="UTF-8") as pfconf:
            pfconf.write("""#ca.lentoapp
anchor "ca.lentoapp"
load anchor "ca.lentoapp" from "/etc/pf.anchors/ca.lentoapp\"""")

        if not Path(Config.PF_ANCHOR_PATH).exists() or os.stat(Config.PF_ANCHOR_PATH).st_size == 0:
            with open(Config.PF_ANCHOR_PATH, "w", encoding="UTF-8") as anchor:
                anchor.write("""# Options
set block-policy drop
set fingerprints \"/etc/pf.os\"
set ruleset-optimization basic
set skip on lo0

#
# Rules for Lento blocks
#""")

    async def block_website(self, website):
        """pf requires certain syntax in a few config files to block sites."""

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
        new_lines = []
        with open(Config.PF_CONFIG_PATH, "r", encoding="UTF-8") as pfconf:
            for line in pfconf:
                if "ca.lentoapp" not in line:
                    new_lines.append(line)
        with open(Config.PF_CONFIG_PATH, "w", encoding="UTF-8") as pfconf:
            pfconf.write("".join(new_lines))
