
import psutil
import ctypes
from functions.logger import Logger
from types import NoneType


class LASTINPUTINFO(ctypes.Structure): _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint),]


class Functions(object):
    logger: Logger = None
    config = None
    def __init__(self, logger: Logger, config):
        from data.activity import Config
        self.logger = logger
        self.config: Config = config
    def get_idle_duration(self):
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(lii)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0

    def get_running_processes(self):
        processes = set()
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info["name"]
                if name:
                    processes.add(name.lower())
            except:
                pass
        return processes

    def detect_activity(self, act: list[dict]):
        idle_time = self.get_idle_duration()
        running = self.get_running_processes()

        if idle_time > 0: self.logger.debug("time in afk:", idle_time)
        new_activity = None

        for activity in act:
            if activity.get("idle") or activity.get("chill"):
                continue
            for process in activity["processes"]:
                if process.lower() in running:
                    new_activity = activity

        if idle_time >= self.config.time_idle - self.config.sleep:
            for activity in act:
                if activity.get("idle"):
                    new_activity = activity
        else:
            for activity in act:
                if activity.get("chill") and isinstance(new_activity, NoneType):
                    new_activity = activity


        return new_activity