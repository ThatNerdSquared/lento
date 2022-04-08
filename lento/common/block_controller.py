import datetime
import subprocess
import pickle
from peewee import BlobField, CharField, DoesNotExist, Model, SqliteDatabase
import lento.common.cards_management as CardsManagement
from lento.config import Config
from lento import utils

db = SqliteDatabase(Config.DB_PATH)


class BlockTimer(Model):
    website = CharField()
    data = BlobField()

    class Meta:
        database = db


class BlockController:
    def __init__(self):
        super().__init__()

    def start_block(self, card_to_use: str, lasts_for: int):
        CardsManagement.activate_block_in_settings(card_to_use)
        bundled_binary_path = utils.get_data_file_path("lentodaemon")
        commands = [
            ("osascript -e 'do shell script"
                f" \"cp \\\"{bundled_binary_path}\\\""
                f" \\\"{Config.DAEMON_BINARY_PATH}\\\"\""
                " with administrator privileges'"),
            " ".join([
                f"\"{str(Config.DAEMON_BINARY_PATH)}\"",
                f"\"{card_to_use}\"",
                str(lasts_for)
            ])
        ]
        result = []
        for cmd in commands:
            result.append(subprocess.call(cmd, shell=True))
        return result

    def end_block(self):
        CardsManagement.deactivate_block_in_settings()
        cmd = ("osascript -e 'do shell script"
               f" \"rm \\\"{Config.DAEMON_BINARY_PATH}\\\""
               "\" with administrator privileges'")
        return subprocess.call(cmd, shell=True)

    def get_remaining_block_time(self) -> tuple[int, int, int]:
        try:
            timer = BlockTimer.get(BlockTimer.website == "_main")
        except DoesNotExist:
            return (0, 0, 0)
        db.close()

        data = pickle.loads(timer.data)
        time_diff = (
            data["time_started"]+datetime.timedelta(seconds=data["lasts_for"])
        ) - datetime.datetime.now()

        seconds = time_diff.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return (int(hours), int(minutes), int(seconds))
