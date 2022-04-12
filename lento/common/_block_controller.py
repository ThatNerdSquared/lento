import datetime
import pickle
import platform
from abc import ABC, abstractmethod
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


class BlockController(ABC):
    def __init__(self):
        super().__init__()
        db.create_tables([BlockTimer])
        db.close()

    @abstractmethod
    def daemon_launch(self):
        """Will be implemented by children for each platform."""

    @abstractmethod
    def daemon_takedown(self):
        """Will be implemented by children for each platform."""

    def start_block(self, card_to_use: str, lasts_for: int):
        CardsManagement.activate_block_in_settings(card_to_use)
        bundled_binary_path = utils.get_data_file_path(
            "lentodaemon" if platform.system() == "Darwin" else "lentodaemon.exe"  # noqa: E501
        )
        return self.daemon_launch(bundled_binary_path, card_to_use, lasts_for)

    def end_block(self):
        CardsManagement.deactivate_block_in_settings()
        return self.daemon_takedown()


    def get_remaining_block_time(self):
        try:
            timer = BlockTimer.get(BlockTimer.website == "_main")
        except DoesNotExist:
            return 0
        db.close()

        data = pickle.loads(timer.data)
        time_diff = (
            data["time_started"]+datetime.timedelta(seconds=data["lasts_for"])
        ) - datetime.datetime.now()

        seconds = time_diff.total_seconds()
        return int(seconds)
