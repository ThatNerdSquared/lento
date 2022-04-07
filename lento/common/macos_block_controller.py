import subprocess
import textwrap
from lento import utils
from lento.common._block_controller import BlockController
from lento.config import Config


class macOSBlockController(BlockController):
    """Lento block controller using `launchd` on macOS."""

    def __init__(self):
        super().__init__()

    def start_daemon(self, card_to_use: str, lasts_for: int):
        plist_contents = textwrap.dedent(f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
              <dict>
                <key>Label</key>
                <string>{Config.REVERSED_DOMAIN}</string>
                <key>Program</key>
                <string>{Config.DAEMON_BINARY_PATH}</string>
                <key>KeepAlive</key>
                <true/>
                <key>ProgramArguments</key>
                <array>
                    <string>{card_to_use}</string>
                    <string>{lasts_for}</string>
                    <string>{Config.HOME_FOLDER}</string>
                </array>
                <key>StandardErrorPath</key>
                <string>/tmp/lentodaemon.err</string>
                <key>StandardOutPath</key>
                <string>/tmp/lentodaemon.out</string>
              </dict>
            </plist>
        """).lstrip()  # noqa: E501

        utils.write_to_root_file_macos(
            plist_contents,
            Config.DAEMON_PLIST_PATH
        )
