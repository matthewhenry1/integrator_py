# local imports
import xmatters
import config

# python3 package imports
import logging
import base64
import json
from logging.handlers import RotatingFileHandler
import urllib.parse
import datetime
import csv

# main process
def main() -> object:
    current_date_time = datetime.datetime.now()
    total = 9000
    page_size = 100
    thread_count = 10
    param_data = {
        "filter_url": 'at=' + str(current_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')),
        "event_id": "123"
    }


    xm_collection.get_collection(xm_event.get_user_deliveries, total, page_size, param_data, thread_count)

if __name__ == "__main__":
    # configure the logging
    logging.basicConfig(level=config.logging["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.logging["file_name"], maxBytes=config.logging["max_bytes"],
                                                      backupCount=config.logging['back_up_count'])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"],
                                       config.environment["password"])
    xm_event = xmatters.xMattersEvent(environment)
    xm_collection = xmatters.xMattersCollection(environment)

    main()  # execute the main process

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))
