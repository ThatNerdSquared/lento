import logging

from peewee import (
    DateTimeField,
    DoesNotExist,
    DoubleField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

from lento import daemon
from lento.config import Config
from lento.daemon.block_item import AppBlockItem, NotificationItem, WebsiteBlockItem

db = SqliteDatabase(None)

"""
Database model definitions
Each model defines the columns of a separate table
Root Model must have "class Meta" definition
"""


class BlockItemModel(Model):
    """
    Each BlockItem has an 'owner' to know
    which TimerTask this item belongs to
    """

    owner = TextField()
    is_soft_block = IntegerField()
    allow_interval = IntegerField()
    last_asked = DateTimeField()
    is_allowed = IntegerField()
    popup_msg = TextField()

    class Meta:
        database = db


class AppBlockItemModel(BlockItemModel):
    procname = TextField()


class WebsiteBlockItemModel(BlockItemModel):
    website_url = TextField()


class NotificationItemModel(Model):
    owner = TextField()
    message = TextField()
    interval = DoubleField()

    class Meta:
        database = db


class TimerTaskModel(Model):
    name = TextField()
    end_time = DateTimeField()

    class Meta:
        database = db


class DBController:
    """
    Class handling saving objects to a database
    """

    # class property to determine if the database
    # has been initialized before. This is to avoid
    # unneccessary repeated database initialization
    initialized = False

    @classmethod
    def init(cla):
        # only initialize the database if it has
        # not been initialized before
        if not cla.initialized:
            logging.info("Initializing database")
            db.init(Config.DB_PATH)
            db.create_tables(
                [
                    BlockItemModel,
                    AppBlockItemModel,
                    WebsiteBlockItemModel,
                    NotificationItemModel,
                    TimerTaskModel,
                ]
            )
            db.close()

            # once initialized, set the database
            # initialized flag
            logging.info("Done initializing database")
            cla.initialized = True

    @classmethod
    def get_all_timer_tasks(cla):
        """
        Returns all TimerTask object saved in the database
        """
        try:
            timer_tasks = TimerTaskModel.select()
            db.close()
        except DoesNotExist:
            return None

        task_list = []

        # iterate each TimerTaskModel and recover
        # the TimerTask object from TimerTaskModel
        for timer_task in timer_tasks:
            task = cla._build_timer_task(timer_task)
            task_list.append(task)

        return task_list

    @classmethod
    def save_timer_task(cla, task):
        """
        Save the TimerTask object and its associated block
        items and notification items to database

        Parameters
        task: the TimerTask object to save
        """
        logging.info("Saving task {} to db...".format(task.name))

        # add the TimerTask to database
        TimerTaskModel.create(name=task.name, end_time=task.end_time)

        # add AppBlockItems from the TimerTask
        # to the database
        for app in task.blocked_apps:
            app_item = task.blocked_apps[app]
            AppBlockItemModel.create(
                owner=task.name,
                is_soft_block=app_item.is_soft_block,
                last_asked=app_item.last_asked,
                is_allowed=app_item.is_allowed,
                procname=app_item.procname,
                allow_interval=app_item.allow_interval,
                popup_msg=app_item.popup_msg,
            )

        # add WebsiteBlockItems from the TimerTask
        # to the database
        for website in task.blocked_websites:
            website_item = task.blocked_websites[website]
            WebsiteBlockItemModel.create(
                owner=task.name,
                is_soft_block=website_item.is_soft_block,
                last_asked=website_item.last_asked,
                is_allowed=website_item.is_allowed,
                website_url=website_item.website_url,
                allow_interval=website_item.allow_interval,
                popup_msg=website_item.popup_msg,
            )

        # add NotificationItems from the TimerTask
        # to the database
        for notification in task.notifications:
            notification_item = task.notifications[notification]
            NotificationItemModel.create(
                owner=task.name,
                message=notification_item.message,
                interval=notification_item.interval,
            )

        db.close()

    @classmethod
    def remove_timer_task(cla, name):
        """
        Deletes a TimerTask object and its associated block
        items and notification items from database

        Parameters
        name: name of the TimerTask to delete
        """
        try:
            logging.info("Removing task {} from db...".format(name))

            # remove apps associated with the TimerTask
            AppBlockItemModel.delete().where(AppBlockItemModel.owner == name).execute()

            # remove websites associated with the TimerTask
            WebsiteBlockItemModel.delete().where(
                WebsiteBlockItemModel.owner == name
            ).execute()

            # remove notifications associated with the TimerTask
            NotificationItemModel.delete().where(
                NotificationItemModel.owner == name
            ).execute()

            # remove the TimerTask last
            TimerTaskModel.delete().where(TimerTaskModel.name == name).execute()

            db.close()

        except DoesNotExist:
            return False

        return True

    @classmethod
    def get_website_item(cla, owner, website_url):
        """
        Fetches a WebsiteBlockItem object given an
        owner and a website url

        Parameters
        owner: the name of the TimerTask object owning
            the WebsiteBlockItem object
        website_url: the website URL associated with
            the WebsiteBlockItem object

        Returns
        the corresponding WebsiteBlockItem object,
        None if not corresponding object exists
        """
        website_model = None

        try:
            website_model = WebsiteBlockItemModel.get(
                WebsiteBlockItemModel.owner == owner,
                WebsiteBlockItemModel.website_url == website_url,
            )
        except DoesNotExist:
            return website_model

        # build WebsiteBlockItem from WebsiteBlockItemModel
        website_item = WebsiteBlockItem(
            website_model.website_url, website_model.owner, website_model.is_soft_block
        )
        website_item.last_asked = website_model.last_asked
        website_item.is_allowed = website_model.is_allowed
        website_item.allow_interval = website_model.allow_interval
        website_item.popup_msg = website_model.popup_msg

        return website_item

    @classmethod
    def update_website_record(cla, owner, website_url, last_asked, is_allowed):
        """
        Updates the last_asked and is_allowed fields of the
        WebsiteBlockItem object associated with the owner and
        website URL

        Parameters
        owner: the name of the TimerTask object owning
            the WebsiteBlockItem object
        website_url: the website URL associated with
            the WebsiteBlockItem object
        last_ask: the last asked date for the website item
        is_allowed: whether the website item was allowed the
            last time it was asked

        Returns:
        True if record is found and update is successful
        False otherwise
        """
        record = None

        try:
            record = WebsiteBlockItemModel.get(
                WebsiteBlockItemModel.owner == owner,
                WebsiteBlockItemModel.website_url == website_url,
            )
        except DoesNotExist:
            return False

        if record:
            record.last_asked = last_asked
            record.is_allowed = is_allowed
            record.save()
            return True

        return False

    @classmethod
    def update_app_record(cla, owner, procname, last_asked, is_allowed):
        """
        Updates the last_asked and is_allowed fields of the
        AppBlockItem object associated with the owner and
        process name

        Parameters
        owner: the name of the TimerTask object owning
            the AppBlockItem object
        procname: the process name associated with the
            AppBlockItem object
        last_ask: the last asked date for the app item
        is_allowed: whether the app item was allowed the
            last time it was asked

        Returns:
        True if record is found and update is successful
        False otherwise
        """
        record = None

        try:
            record = AppBlockItemModel.get(
                AppBlockItemModel.owner == owner, AppBlockItemModel.procname == procname
            )
        except DoesNotExist:
            return False

        if record:
            record.last_asked = last_asked
            record.is_allowed = is_allowed
            record.save()
            return True

        return False

    @classmethod
    def _build_timer_task(cla, timer_task_model):
        """
        Recovers the complete TimerTask object from
        TimerTaskModel

        Parameters
        timer_task_model: the TimerTaskModel object

        Returns:
        the recovered TimerTask object
        """

        # initialize timer task object
        timer_task = daemon.timer_task.TimerTask()
        timer_task.name = timer_task_model.name
        timer_task.end_time = timer_task_model.end_time

        # build associated blocked apps dictionary
        app_model_list = AppBlockItemModel.select().where(
            AppBlockItemModel.owner == timer_task.name
        )

        for app_model in app_model_list:
            app_item = AppBlockItem(
                app_model.procname, app_model.owner, app_model.is_soft_block
            )
            app_item.last_asked = app_model.last_asked
            app_item.is_allowed = app_model.is_allowed
            app_item.allow_interval = app_model.allow_interval
            app_item.popup_msg = app_model.popup_msg

            timer_task.blocked_apps[app_model.procname] = app_item

        # build associated blocked websites dictionary
        website_model_list = WebsiteBlockItemModel.select().where(
            WebsiteBlockItemModel.owner == timer_task.name
        )

        for website_model in website_model_list:
            website_item = WebsiteBlockItem(
                website_model.website_url,
                website_model.owner,
                website_model.is_soft_block,
            )
            website_item.last_asked = website_model.last_asked
            website_item.is_allowed = website_model.is_allowed
            website_item.allow_interval = website_model.allow_interval
            website_item.popup_msg = website_item.popup_msg

            url = website_model.website_url
            timer_task.blocked_websites[url] = website_item

        # build associated notifications list
        notification_model_list = NotificationItemModel.select(
            NotificationItemModel.owner == timer_task.name
        )

        for notification_model in notification_model_list:
            notification_item = NotificationItem(
                notification_model.message,
                notification_model.interval,
                notification_model.owner,
            )

            timer_task.notifications.append(notification_item)

        return timer_task
