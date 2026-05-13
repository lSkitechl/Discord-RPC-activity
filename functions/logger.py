from pathlib import Path
from datetime import datetime

class Logger(object):
    """
    ### A class for displaying my project's logs.

    ##### Default level logging:
    `Logger.level(Logger.types.INFO)`

    ##### Name Logger:
    Supports different names for different streams; by default, it has no name.

    `Logger(name="Your thread name")`

    ##### Support levels logging:
        `logger.debug`
        `logger.info`
        `logger.warn`
        `logger.error`
        `logger.crit`
    """

    thread_name = ""
    color = True

    log_directory = "logs"
    max_file_size = 1024 * 1024 * 5

    def __init__(self, name=""):
        self.thread_name = name or "Main"
        ph = Path(self.log_directory)
        if not ph.exists(): ph.mkdir(parents=True, exist_ok=True)

    class colors():
        green = "\033[32m"
        yellow = "\033[33m"
        red = "\033[31m"
        reset = "\033[0m"
        light_red = "\033[1;31m"

    class types():
        ERROR = ["error", "critical"]
        WARN = ["warn", "error", "critical"]
        INFO = ["info", "warn", "error", "critical"]
        DEBUG = ["debug", "info", "warn", "error", "critical"]

    logging = types.INFO

    def _get_log_path(self): return Path(self.log_directory) / f"{self.thread_name}.log"

    def _rotate_log_if_needed(self, log_path: Path):
        if not log_path.exists():
            return

        if log_path.stat().st_size >= self.max_file_size:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            rotated_file = log_path.parent /f"{log_path.stem}_{timestamp}{log_path.suffix}"
            log_path.rename(rotated_file)

    def _write_file(self, text):
        log_path = self._get_log_path()
        self._rotate_log_if_needed(log_path)
        with open(log_path, "a", encoding="utf-8") as f: f.write(text + "\n")

    def _log(self, tag, text, color, key):
        if key in self.logging:
            prefix = f"[{self.thread_name}]" if self.thread_name else ""
            message = f"[{datetime.now()}] [{tag}]{f' {prefix}' if prefix else ''} {' '.join(str(x) for x in text)}"
            if self.color: print(f"{color}{message}{self.colors.reset}")
            else: print(message)
            self._write_file(message)

    @classmethod
    def level(cls, log_level):
        cls.logging = log_level

    @classmethod
    def is_color(cls, color):
        cls.color = color

    @classmethod
    def file_config(cls, max_size_mb=5, directory=""):
        """
        directory - log folder
        max_size_mb - maximum size of a single file in MB
        """
        if not directory: cls.log_directory = directory
        cls.max_file_size = max_size_mb * 1024 * 1024
        Path(directory).mkdir(parents=True, exist_ok=True)

    def debug(self, *text):self._log("DEBUG", text, "", "debug")
    def info(self, *text):self._log("INFO", text, self.colors.green, "info")
    def warn(self, *text):self._log("WARN", text, self.colors.yellow, "warn")
    def error(self, *text):self._log("ERROR", text, self.colors.light_red, "error")
    def crit(self, *text):self._log("CRITICAL", text, self.colors.red, "critical")