import sys
import json
import time
import psutil
import platform
import subprocess
from lento.config import Config
from multiprocessing.connection import Client

# TODO: daemonize lentodaemon on Windows


class LentoDaemonInterface:
    """
    Class that provides an Application Programming Interface (API)
    to lentodaemon
    """

    def __init__(self, logger):
        """
        Parameters
        logger: python logger to log all LentoDaemonInterface to
        """
        self.logger = logger

    def launch_daemon(self):
        """
        Launches lentodaemon if it is not yet running
        """

        # if daemon is already running, don't need to launch it again
        if self.is_daemon_running():
            self.logger.info("lentodaemon is already launched & running")
            return True

        # remove "daemon_port" key from lentosettings.json
        self._remove_port_from_settings()

        success = False
        match platform.system():
            case "Darwin":
                success = subprocess.Popen(
                    [
                        "launchctl",
                        "load",
                        str(Config.DAEMON_PLIST_PATH),
                    ]
                )
            case "Windows":
                self.logger.info("lentodaemon unsupported on Windows")

        if not success:
            self.logger.error("failed to launch daemon")
            return False

        # after daemon is launched, wait for daemon to be ready
        # before returning
        self.logger.info("waiting for daemon to be ready")
        while not self.is_daemon_ready():
            time.sleep(1)

        self.logger.info("daemon is launched and running")

        return True

    def terminate_daemon(self):
        """
        Terminate lentodaemon if it is already running
        """

        # if daemon is not running, don't need to terminate
        if not self.is_daemon_running():
            self.logger.info("lentodaemon is not running, ignore termination")

        # only terminate the daemon if it is ready
        if self.is_daemon_ready():
            daemon_port = self._get_daemon_port()
            if daemon_port:
                # send message to daemon to clean up first
                # before terminating the daemon process
                self.logger.info("messaging daemon to cleanup")
                address = ("localhost", daemon_port)

                request = {"command": "cleanup"}

                conn = Client(address, authkey=b"lento")
                conn.send(request)
                msg = conn.recv()
                conn.send("close")
                conn.close()

                self.logger.info("daemon respone: {}".format(msg))

                # delete "daemon_port" key from lentosettings.json
                self._remove_port_from_settings()

        match platform.system():
            case "Darwin":
                return subprocess.Popen(
                    [
                        "launchctl",
                        "unload",
                        str(Config.DAEMON_PLIST_PATH),
                    ]
                )
            case "Windows":
                self.logger.info("lentodaemon unsupported on Windows")
                return False

        return False

    def is_daemon_running(self):
        """
        Returns if "lentodaemon" process is running
        """

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                procname = proc.name()
            except psutil.NoSuchProcess:
                continue
            except psutil.ZombieProcess:
                continue

            if procname == "lentodaemon":
                return True

        return False

    def is_daemon_ready(self):
        """
        Returns if "lentodaemon" process is running and
        daemon is ready to accept incoming messages
        """
        is_running = self.is_daemon_running()
        daemon_port = self._get_daemon_port()

        return is_running and (daemon_port is not None)

    def start_block_timer(self, info_dict, time_to_run, launch_daemon=False):
        """
        Send messages to daemon to start a block timer task

        Parameters
        info_dict: dictionary of timer task info
        time_to_run: amount of time to run the task for
        """

        # plug in the task interval to info dictionary
        info_dict["duration"] = time_to_run

        self.logger.info("starting block timer task {}".format(info_dict.get("name")))

        if launch_daemon:
            # if daemon is not ready, launch the daemon
            if not self.is_daemon_ready():
                self.logger.info("lento daemon is not ready, starting daemon")
                if not self.launch_daemon():
                    self.logger.error("failed to launch lentodaemon")
                    return False

        # get the port that daemon is listening at
        daemon_port = self._get_daemon_port()

        self.logger.info("daemon port is {}".format(daemon_port))
        if daemon_port is None:
            self.logger.error("failed to find daemon listening port")
            return False

        # send the request
        self.logger.info("sending block timer task info {}".format(info_dict))

        address = ("localhost", daemon_port)

        request = {"command": "start_timer", "payload": info_dict}

        conn = Client(address, authkey=b"lento")
        conn.send(request)
        msg = conn.recv()
        conn.send("close")
        conn.close()

        self.logger.info("daemon response: {}".format(msg))

        return msg == "OK"

    def _get_daemon_port(self):
        """
        Read "daemon_port" key from lentosettings.json
        """
        SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
        daemon_port = SETTINGS.get("daemon_port")

        return daemon_port

    def _remove_port_from_settings(self):
        """
        Delete "daemon_port" key from lentosettings.json
        """
        SETTINGS = json.loads(Config.SETTINGS_PATH.read_text())
        if SETTINGS.get("daemon_port"):
            self.logger.info("removing deamon port from Settings json")
            SETTINGS.pop("daemon_port")
            Config.SETTINGS_PATH.write_text(json.dumps(SETTINGS))
