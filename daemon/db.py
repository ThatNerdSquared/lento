import datetime
import pickle
from peewee import BlobField, CharField, DoesNotExist, Model, SqliteDatabase
from lento.config import Config

db = SqliteDatabase(Config.DB_PATH)


class BlockTimer(Model):
    website = CharField()
    data = BlobField()

    class Meta:
        database = db


class DBController:

    def __init__(self):
        db.create_tables(BlockTimer)

    def create_host_timer(self, website, is_allowed):
        data = {
            "last_asked": datetime.datetime.now(),
            "is_allowed": is_allowed
        }
        BlockTimer.create(website=website, data=pickle.dumps(data))

    def get_site_entry(self, website):
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
        except DoesNotExist:
            return None
        return pickle.loads(timer.data)

    def check_if_site_blocked(self, website):
        """
        Check if a given website is blocked.
        Returns a bool corresponding to the block state.
        """
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
        except DoesNotExist:
            return False
        data = pickle.loads(timer.data)
        if data.is_allowed:
            if (
                datetime.datetime.now() - data.last_asked
            ).total_seconds() / 60.0 >= 15:
                timer.is_allowed = False
                timer.save()
                return False
        else:
            return False
        return True

    def update_site(self, website, is_allowed):
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
        except DoesNotExist:
            return self.create_host_timer(website, is_allowed)
        timer.is_allowed = is_allowed
        timer.last_asked = datetime.datetime.now()
        timer.save()
