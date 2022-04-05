import subprocess
import textwrap
from lento.common._block_controller import BlockController
from lento.config import Config


class macOSBlockController(BlockController):
    """Lento block controller using `launchd` on macOS."""

    def __init__(self):
        super().__init__()

    def start_daemon(self, card_to_use: str, lasts_for: int):
        plist_contents = textwrap.dedent(f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC -//Apple Computer//DTD PLIST 1.0//EN http://www.apple.com/DTDs/PropertyList-1.0.dtd >
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
                    <string><CARD_TO_USE>{card_to_use}</string>
                    <string><LASTS_FOR>{lasts_for}</string>
                </array>
              </dict>
            </plist>
        """).lstrip()  # noqa: E501

        Config.DAEMON_PLIST_PATH.write_text(plist_contents)
        commands = [
            f"sudo launchctl load {Config.DAEMON_PLIST_PATH}",
            f"sudo launchctl start {Config.REVERSED_DOMAIN}"
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result
