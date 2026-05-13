import json, os
from functions.logger import Logger


class Gateway(object):
    path = str()
    logger: Logger = None

    def __init__(self, path: str, logger: Logger = None):
        self.path = path
        self.logger = logger

        if not self._check_exist():
            with open(self.path, "w+", encoding="UTF-8") as file: 
                json.dump([], file, indent=3, ensure_ascii=False)

    def _check_exist(self): return os.path.isfile(path=self.path)

    def read(self):
        with open(self.path, "r", encoding="UTF-8") as file: 
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError as err:
                self.logger.warn(err)
                return []

    def write(self, data: list) -> bool:
        """
Returns `True` if successful.

If unsuccessful, outputs a log with `WARN` and returns `False`.
        """
        try: 
            with open(self.path, "w", encoding="UTF-8") as file: json.dump(data, file, indent=3, ensure_ascii=False)
        except Exception as err:
            self.logger.warn(err)
            return False
        else: return True
