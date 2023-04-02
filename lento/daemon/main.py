import json
import sys
import socket
import logging
import multiprocessing
from lento.config import Config
from lento.daemon.util.db import DBController
from multiprocessing.connection import Listener
from lento.daemon.timer_task import TimerTask
from logging.handlers import RotatingFileHandler
from lento.daemon.alert.lento_notif import LentoNotif


class LentoDaemon:
    """
    Class that encapsulates the daemon
    """

    def __init__(self, num_acceptors):
        self.task_dict = {}
        self.main_timer = None
        self.task = None
        self.num_acceptors = num_acceptors

    def entry(self):
        """
        Entry point of the daemon
        """
        DBController.init()

        # Check if there are any existing tasks in the database.
        # If there are, resume the task
        logging.info("Checking for existing tasks in database")
        task_list = DBController.get_all_timer_tasks()

        if len(task_list) > 0:
            logging.info("Loaded {} tasks from db".format(len(task_list)))
            # always just load the first task since we assume the
            # daemon can only handle one task at a time
            self.task = task_list[0]
            self.task.print()

            # assign completion handler to task recovered from
            # database since tasks recovered from databases
            # are not initialized with completion handler
            self.task.completion_handler = self.completion_handler

            # if task is already complete, remove it
            if self.task.is_complete():
                logging.info("Task {} is already complete".format(self.task.name))
                DBController.remove_timer_task(self.task.name)
                self.task = None

            # if task is still ongoing, start it
            else:
                logging.info("Starting saved task {}".format(self.task.name))
                self.task.start(self.num_acceptors)

        else:
            logging.info("No tasks from database")

        # get an open port on device
        port = self._find_open_port()
        address = ("localhost", port)  # family is deduced to be 'AF_INET'

        # IPC setup, code taken from
        # https://stackoverflow.com/questions/6920858/interprocess-communication-in-python

        logging.info("Listening for incoming connection at {}".format(address))
        listener = Listener(address, authkey=b"lento")

        # save the port that the daemon is listening from
        # in lentosettings.json under "daemon_port" key
        self._save_port_to_settings(port)

        while True:
            conn = listener.accept()
            logging.info("Incoming connection!")

            # once a connection is made, the
            # connection will be alive until
            # "close" message is received
            while True:
                msg = conn.recv()

                if msg == "close":
                    conn.close()
                    break

                error_msg = self._handle_msg(msg)

                if not error_msg:
                    conn.send("OK")
                else:
                    conn.send(error_msg)

        listener.close()

    def completion_handler(self):
        """
        Mathod that is called whenever a TimerTask is complete
        Here we set the "task" field to None so we are ready
        for another task
        """
        logging.info("Task {} complete".format(self.task.name))
        LentoNotif(
            "Lento: Block Complete",
            "Task {} complete, block deactivated".format(self.task.name),
        ).send_banner()
        self.task = None

    def _handle_msg(self, request):
        """
        Handles the request dictionary
        """

        # parse the command and payload, request
        # messages are expected to have the following
        # format:
        # {
        #   "command": command_str,
        #   "payload": payload_dict
        # }
        command = request.get("command")
        info_dict = request.get("payload")

        # handle start timer message
        if command == "start_timer":
            logging.info("Handling start timer...")

            # only run a task if there are no other
            # task running, the daemon cannot take
            # multiple tasks at once
            if self.task is None:
                self._run_task(info_dict)
                return None
            else:
                logging.info(
                    "Ignoring start timer request, "
                    "{} already running".format(self.task.name)
                )
                return "Task {} already running".format(self.task.name)

        # handle clean up message
        elif command == "cleanup":
            logging.info("Cleaning up daemon...")

            # clean up the current task
            if self.task is not None:
                logging.info("Cleaning up task {}".format(self.task.name))
                self.task.cleanup()

        return "Invalid Command: {}".format(command)

    def _run_task(self, info_dict):
        """
        Create a task from an info dictionary and launch it
        """
        self.task = TimerTask(info_dict, self.completion_handler)
        logging.info("Launching task {}".format(self.task.name))
        self.task.start(self.num_acceptors)
        self.task.print()

    def _find_open_port(self):
        """
        Use socket's built-in ability to find an open port
        Code taken from https://gist.github.com/jdavis/4040223

        Returns:
        open port
        """
        sock = socket.socket()
        sock.bind(("", 0))
        _, port = sock.getsockname()

        return port

    def _save_port_to_settings(self, port):
        """
        Saves a port to lentosettings.json file under
        key "daemon_port"
        """
        SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
        SETTINGS["daemon_port"] = port
        Config.SETTINGS_PATH.write_text(json.dumps(SETTINGS))


def main():
    # setup logging: set up two logging handlers to log
    # both to file (RotatingFileHandler) and to console
    # (StreamHandler)
    log_file_path = Config.APPDATA_PATH / "lentodaemon.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - pid:%(process)d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RotatingFileHandler(
                log_file_path,
                mode="a",
                maxBytes=5 * 1024 * 1024,
                backupCount=2,
                encoding=None,
                delay=0,
            ),
            logging.StreamHandler(),
        ],
    )

    # multiprocessing hack for packager
    multiprocessing.freeze_support()

    logging.info("Daemon start")

    num_acceptors = sys.argv[-1]  # number of acceptors for Proxy

    # start daemon
    daemon = LentoDaemon(num_acceptors)
    daemon.entry()


if __name__ == "__main__":
    main()
