import datetime
import pickle
from peewee import BlobField, CharField, DoesNotExist, Model, SqliteDatabase
from lento.config import Config


db = SqliteDatabase(Config.DB_PATH)


class Record(Model):
    key = CharField()
    data = BlobField()

    class Meta:
        database = db


class NotifsController:

    def __init__(self):
        db.create_tables([Record])
        db.close()

    def set_up_notifs(self, notifs_dict):
        self.create_last_fired_record(notifs_dict)
        self.create_visit_triggers(notifs_dict)
        self.add_notifs_to_db(notifs_dict)

    def create_last_fired_record(self, notifs_dict):
        data = {}
        for item in notifs_dict.keys():
            if (
                notifs_dict[item]["enabled"] and
                notifs_dict[item]["time_interval_trigger"] is not None
            ):
                data[item] = {
                    "last_fired": datetime.datetime.now(),
                    "interval": notifs_dict[item]["time_interval_trigger"]
                }
        Record.create(key="_lastfired", data=pickle.dumps(data))
        db.close()

    def create_visit_triggers(self, notifs_dict):
        data = {}
        for item in notifs_dict.keys():
            if notifs_dict[item]["enabled"]:
                for trigger in notifs_dict[item]["blocked_visit_triggers"]:
                    try:
                        data[trigger] = data[trigger].append(item)
                    except KeyError:
                        data[trigger] = [item]
        Record.create(key="_visittriggers", data=pickle.dumps(data))
        db.close()

    def add_notifs_to_db(self, notifs_dict):
        for item in notifs_dict.keys():
            if notifs_dict[item]["enabled"]:
                Record.create(key=item, data=pickle.dumps(notifs_dict[item]))
        db.close()

    def get_triggered_notifs(self, trigger):
        try:
            visit_triggers = Record.get(Record.key == "_visittriggers")
            db.close()
        except DoesNotExist:
            return None

        data = pickle.loads(visit_triggers.data)
        if not data[trigger]:
            return None

        triggered_notifs = {}
        for item in data[trigger]:
            notif_record = Record.get(Record.key == item)
            triggered_notifs[item] = pickle.loads(notif_record.data)
        db.close()
        return triggered_notifs

    def check_for_time_triggers(self):
        try:
            last_fired_record = Record.get(Record.key == "_lastfired")
            db.close()
        except DoesNotExist:
            return None

        last_fired = pickle.loads(last_fired_record.data)
        notifs_to_fire = {}
        for item in last_fired.keys():
            if (
                datetime.datetime.now() - last_fired[item]["last_fired"]
            ).total_seconds() >= float(last_fired[item]["interval"]):
                notif_record = Record.get(Record.key == item)
                notifs_to_fire[item] = pickle.loads(notif_record.data)
        db.close()
        return notifs_to_fire

    def update_fire_date(self, notif_id):
        try:
            last_fired_record = Record.get(Record.key == "_lastfired")
            db.close()
        except DoesNotExist:
            return None
        data = pickle.loads(last_fired_record.data)
        try:
            data[notif_id]["last_fired"] = datetime.datetime.now()
            last_fired_record.data = pickle.dumps(data)
            last_fired_record.save()
        except KeyError:
            return
        db.close()

    def fire_notifs(self, notifs_to_fire):
        for item in notifs_to_fire.keys():
            notif = notifs_to_fire[item]
            name = notif["name"]
            title = notif["title"]
            body = notif["body"]
            notif_type = notif["type"]
            print(f"===START NOTIFICATION: {name}===")
            print(f"TITLE {title} WITH BODY {body} OF TYPE {notif_type}")
            print(f"===END NOTIFICATION: {name}===")
            self.update_fire_date(item)

    def clear_notifs(self):
        Record.delete().where(Record.key is not None).execute()
        db.close()
        print("Notifs cleared!")
