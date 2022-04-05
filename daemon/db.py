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
        db.create_tables([BlockTimer])
        db.close()

    def create_main_timer(self, lasts_for):
        data = {
            "time_started": datetime.datetime.now(),
            "lasts_for": float(lasts_for)
        }
        BlockTimer.create(website="_main", data=pickle.dumps(data))
        db.close()

    def check_if_block_is_over(self):
        timer = BlockTimer.get(BlockTimer.website == "_main")
        db.close()
        data = pickle.loads(timer.data)
        if (
            datetime.datetime.now() - data["time_started"]
        ).total_seconds() >= float(data["lasts_for"]):
            return True
        else:
            return False

    def create_host_timer(self, website, is_allowed):
        data = {
            "last_asked": datetime.datetime.now(),
            "is_allowed": is_allowed
        }
        BlockTimer.create(website=website, data=pickle.dumps(data))
        db.close()

    def get_site_entry(self, website):
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
            db.close()
        except DoesNotExist:
            return None
        return pickle.loads(timer.data)

    def check_if_site_allowed(self, website):
        """
        Check if a given website is allowed.
        Returns a bool corresponding to the block state.
        """
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
            db.close()
        except DoesNotExist:
            return False
        data = pickle.loads(timer.data)
        if data["is_allowed"]:
            if (
                datetime.datetime.now() - data["last_asked"]
            ).total_seconds() / 60.0 >= 15:
                data = pickle.loads(timer.data)
                data["is_allowed"] = False
                timer.data = pickle.dumps(data)
                timer.save()
                return False
            else:
                return True
        else:
            return False

    def update_site(self, website, is_allowed):
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
            db.close()
        except DoesNotExist:
            return self.create_host_timer(website, is_allowed)
        data = pickle.loads(timer.data)
        data["is_allowed"] = is_allowed
        data["last_asked"] = datetime.datetime.now()
        timer.data = pickle.dumps(data)
        timer.save()

    def clear_db(self):
        BlockTimer.delete().where(BlockTimer.website is not None).execute()
        db.close()
        print("Database cleared!")
