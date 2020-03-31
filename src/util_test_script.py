# local imports
import xmatters
import config

# python3 package imports
import logging
import json
from logging.handlers import RotatingFileHandler

# main process
def main() -> object:
    """
    -- TEST CASES --
    The below test cases are used in conjunction with integrator_py/src/data/dynamic_teams.csv
    """
    # 1.) Pass: Return specific columns, this should return every occurrence of the targetName
    dynamic_teams_data = dynamic_teams_file.get_rows(["targetName"])
    print(json.dumps(dynamic_teams_data))

    # 2.) Pass: Return all columns and delimiter
    dynamic_teams_data = dynamic_teams_file.get_rows(["*"], None, None, ";")
    print(json.dumps(dynamic_teams_data))

    # 3.) Passed: Return all columns, this should return every occurrence of the targetName
    dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName"}, False, ";")
    print(json.dumps(dynamic_teams_data))

    # 4.) Passed: Return a distinct list of targetNames
    dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName"}, True, ";")
    print(json.dumps(dynamic_teams_data))

    # 5.) Passed: Should only return a distinct list of the passed key/value
    dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName": "Dynamic Teams 2"}, True, ";")
    print(json.dumps(dynamic_teams_data))

    # 6.) Passed: Should return every occurrence of the passed key/value
    dynamic_teams_data = dynamic_teams_file.get_rows(["*"], {"targetName": "Dynamic Teams 2"}, False, ";")
    print(json.dumps(dynamic_teams_data))


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
    dynamic_teams_file = xmatters.Column(config.file["file_name"], config.file["encoding"])

    # execute the main process
    main()

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))