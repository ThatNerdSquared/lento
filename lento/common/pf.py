import os
from pathlib import Path
import socket
import subprocess
from lento.common._firewall import Firewall
from lento.config import Config


class PacketFilter(Firewall):
    """Firewall on macOS."""

    def pre_block(self):
        existing_config = Config.PF_CONFIG_PATH.read_text()
        Config.PF_CONFIG_PATH.write_text(existing_config + """#ca.lentoapp
anchor "ca.lentoapp"
load anchor "ca.lentoapp" from "/etc/pf.anchors/ca.lentoapp\"\n""")
        if not Path(Config.PF_ANCHOR_PATH).exists() or os.stat(Config.PF_ANCHOR_PATH).st_size == 0:
            Config.PF_ANCHOR_PATH.write_text("""# Options
set block-policy drop
set fingerprints \"/etc/pf.os\"
set ruleset-optimization basic
set skip on lo0

#
# Rules for Lento blocks
#\n""")

    def block_website(self, website: str) -> None:
        """Add a website to the list of blocked IP addresses on macOS."""

        ip = socket.gethostbyname(website)

        existing_content = Config.PF_ANCHOR_PATH.read_text()

        Config.PF_ANCHOR_PATH.write_text("\n".join([
            existing_content,
            f"""block return out proto tcp from any to {ip}
block return out proto udp from any to {ip}"""
        ]) + "\n")

    def unblock_websites(self):
        with open(Config.PF_ANCHOR_PATH, "w", encoding="UTF-8") as anchor:
            anchor.write('')
        new_lines = []
        with open(Config.PF_CONFIG_PATH, "r", encoding="UTF-8") as pfconf:
            for line in pfconf:
                if "ca.lentoapp" not in line:
                    new_lines.append(line)
        with open(Config.PF_CONFIG_PATH, "w", encoding="UTF-8") as pfconf:
            pfconf.write("".join(new_lines))
        subprocess.call("/sbin/pfctl -F rules", shell=True)
