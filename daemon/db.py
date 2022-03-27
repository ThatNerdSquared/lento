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

    def check_if_site_allowed(self, website):
        """
        Check if a given website is allowed.
        Returns a bool corresponding to the block state.
        """
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
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
                print(15 - (
                    datetime.datetime.now() - data["last_asked"]
                ).total_seconds() / 60.0)
                return True
        else:
            return False

    def update_site(self, website, is_allowed):
        try:
            timer = BlockTimer.get(BlockTimer.website == website)
        except DoesNotExist:
            return self.create_host_timer(website, is_allowed)
        data = pickle.loads(timer.data)
        data["is_allowed"] = is_allowed
        data["last_asked"] = datetime.datetime.now()
        timer.data = pickle.dumps(data)
        timer.save()

    def clear_db(self):
        BlockTimer.delete().where(BlockTimer.website is not None)
        print("done")
