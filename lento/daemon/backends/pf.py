import socket
import subprocess
import textwrap
from lento.daemon.backends._firewall import Firewall
from lento.config import Config


class PacketFilter(Firewall):
    """Firewall on macOS."""

    def pre_block(self):
        if not Config.PF_CONFIG_PATH.exists():
            Config.PF_CONFIG_PATH.touch()
        existing_config = Config.PF_CONFIG_PATH.read_text()
        Config.PF_CONFIG_PATH.write_text(existing_config + """#io.github.lento
anchor "io.github.lento"
load anchor "io.github.lento" from "/etc/pf.anchors/io.github.lento\"\n""")
        if not Config.PF_ANCHOR_PATH.exists() or Config.PF_ANCHOR_PATH.stat().st_size == 0:  # noqa: E501
            pf_template = textwrap.dedent("""
                # Options
                set block-policy drop
                set fingerprints \"/etc/pf.os\"
                set ruleset-optimization basic
                set skip on lo0

                #
                # Rules for Lento blocks
                #
            """).lstrip()
            Config.PF_ANCHOR_PATH.write_text(pf_template)

    def hardblock_website(self, website: str) -> None:
        """Add a website to the list of blocked IP addresses on macOS."""

        ip = socket.gethostbyname(website)
        blocktext = textwrap.dedent(f"""\
            block return out proto tcp from any to {ip}
            block return out proto udp from any to {ip}
        """)

        Config.PF_ANCHOR_PATH.write_text("\n".join([
            Config.PF_ANCHOR_PATH.read_text().strip(),
            blocktext.strip(),
        ]) + "\n")

    def unblock_websites(self):
        Config.PF_ANCHOR_PATH.write_text("")
        new_lines = []
        pfconf = Config.PF_CONFIG_PATH.read_text()
        for line in pfconf.split("\n"):
            if "io.github.lento" not in line:
                new_lines.append(line)
        Config.PF_CONFIG_PATH.write_text("\n".join(new_lines))
        subprocess.call("/sbin/pfctl -F rules", shell=True)

    def softblock_website(self, website: str) -> None:
        """Add a website to the list of blocked IP addresses on macOS."""

        ip = socket.gethostbyname(website)
        blocktext = textwrap.dedent(f"""\
            rdr pass log on lo0 inet proto tcp from any to {ip} -> 127.0.0.1 port 65531
            rdr pass log on lo0 inet proto udp from any to {ip} -> 127.0.0.1 port 65531
            pass out on en0 route-to lo0 proto tcp from en0 to any keep state
            pass out on en0 route-to lo0 proto udp from en0 to any keep state
            """)  # noqa: E501

        Config.PF_ANCHOR_PATH.write_text("\n".join([
            Config.PF_ANCHOR_PATH.read_text().strip(),
            blocktext.strip(),
        ]) + "\n")
