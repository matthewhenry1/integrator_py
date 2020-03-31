# local imports
import xmatters
import config

# python3 package imports
import logging
import json
from logging.handlers import RotatingFileHandler

# main process
def main() -> object:

    groups = xm_group.get_group_collection('status=ACTIVE')
    log.info("Received Active Groups: " + json.dumps(groups))
    print("Number of Active Groups returned: " + str(len(groups)))

    for group in groups:
        print("Getting On Call Schedule for Group: " + str(group['targetName']))
        group_on_call = xm_on_call.get_on_call_collection("&groups="+group['targetName'])
        log.info("Received On Call Schedule for Group: " + json.dumps(group_on_call))


# entry point when file initiated
if __name__ == "__main__":

    # configure the logging
    logging.basicConfig(level=config.logging["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.logging["file_name"], maxBytes=config.logging["max_bytes"], backupCount=config.logging["back_up_count"])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"], config.environment["password"])
    xm_on_call = xmatters.xMattersOnCall(environment)
    xm_group = xmatters.xMattersGroup(environment)

    # execute the main process
    main()

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))
