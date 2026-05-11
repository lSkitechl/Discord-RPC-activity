import time
from functions.statics import *
from functions.logger import Logger
from data.activity import Activity

current_activity = None
Logger.level(Logger.types.DEBUG)
Logger.is_color(False)
logger = Logger("Main")

acty = Activity(Logger("Activity"))
acty.connect()
while True:
    try:
        activity = acty.functions.detect_activity(acty.get_activity())
        logger.debug(activity)
        if activity != current_activity:
            current_activity = activity
            activity_started = int(time.time())
            if activity is None:
                acty.rpc.clear()
                logger.info("Cleared")
            else:
                acty.rpc.update(
                    details=activity["details"],
                    state=activity["state"],
                    name=activity["name"],
                    large_image=activity["large_image"],
                    small_image=activity["small_image"],
                    small_text="small_text",
                    buttons=acty.config.buttons,
                    large_text=activity["large_text"]
                )
                logger.info(activity['name'])
    except Exception as e: logger.error("ERROR:", e)
    time.sleep(acty.config.sleep)