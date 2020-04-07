# local imports
import xmatters
import config

# python3 package imports
import logging
import json
from logging.handlers import RotatingFileHandler


# main process
def main() -> object:

    dynamic_teams_data = dynamic_teams_file.get_rows(["targetName", "supervisors", "observers", "operand"], {"targetName"}, True, ";")
    log.info("dynamic_teams_data: "+json.dumps(dynamic_teams_data))

    # retrieve the criteria
    for data in dynamic_teams_data:
        log.info("Collecting the criteria:  " + data["targetName"])

        dynamic_teams_criteria = dynamic_teams_file.get_rows(["criterionType", "field", "criterionOperand", "value"], {"targetName": data["targetName"]}, False)
        log.info("dynamic_teams_criteria: " + json.dumps(dynamic_teams_criteria))

        # ensure supervisors is a list type
        if type(data["supervisors"]) is str:
            data["supervisors"] = [data["supervisors"]]

        # build the request payload
        request = {
            "targetName": data["targetName"],
            "criteria": {
                "operand": data["operand"],
                "criterion": []
            },
            "supervisors": xm_person.get_people_ids(data["supervisors"]),
            "observers": []
        }

        # add the criteria
        for criteria in dynamic_teams_criteria:
            request['criteria']['criterion'].append({
                "criterionType": criteria["criterionType"],
                "field": criteria["field"],
                "operand": criteria["criterionOperand"],
                "value": criteria["value"],
            })

        # ensure observers is a list type
        if type(data["observers"]) is str:
            data["observers"] = [data["observers"]]

        # add the observers
        for observer in data['observers']:
            request['observers'].append({"name": observer})

        # execute the creation
        xm_dynamic_teams.create_dynamic_team(request)

# entry point when file initiated
if __name__ == "__main__":

    # configure the logging
    logging.basicConfig(level=config.dynamic_teams['logging']["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.dynamic_teams['logging']["file_name"], maxBytes=config.dynamic_teams['logging']["max_bytes"], backupCount=config.dynamic_teams['logging']["back_up_count"])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"], config.environment["password"])
    xm_dynamic_teams = xmatters.xMattersDynamicTeams(environment)
    xm_person = xmatters.xMattersPerson(environment)
    dynamic_teams_file = xmatters.Column(config.dynamic_teams['file']["file_name"], config.dynamic_teams['file']["encoding"])

    # execute the main process
    main()

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))