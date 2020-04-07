# local imports
import xmatters
import config

# python3 package imports
import logging
import json
from logging.handlers import RotatingFileHandler


# main process
def main() -> object:

    groups = members_file.get_rows(["name", "supervisors", "observers"], {"name"}, True, ";")
    log.info("Executing upload for " + str(len(groups)) + " groups.")

    for group in groups:

        if type(group["supervisors"]) is str:
            group["supervisors"] = [group["supervisors"]]

        group_request = {
            "targetName": group["name"],
            "supervisors": xm_person.get_people_ids(group["supervisors"]),
            "observers": []
        }

        # add the observers
        if type(group["observers"]) is str:
            group["observers"] = [group["observers"]]
        for observer in group['observers']:
            group_request['observers'].append({"name": observer})

        log.info("Creating group:  " + group["name"])

        group_response = xm_group.create_group(group_request)

        if group_response:
            log.info('Group: '+group_request["targetName"]+' successfully created ')
            members = members_file.get_rows(["name", "shift", "member"], {"name": group_request["targetName"]}, False)

            new_data = []
            for data in members:
                new_data.append({
                    "group_id": data['name'],
                    "shift_id": data['shift'],
                    "member_id": data['member'],
                })

            if len(new_data) > 0:
                member_response = xm_collection.create_collection(xm_shift.add_member_to_shift, new_data, config.add_members['thread_count'])
                log.info("Member response: " + str(member_response["response"]))
                log.info("Member errors: " + str(member_response["errors"]))
            else:
                log.info("No requests to execute.")

        else:
            log.info('Group: '+group_request["targetName"]+' creation failed.')

# entry point when file initiated
if __name__ == "__main__":

    # configure the logging
    logging.basicConfig(level=config.add_members['logging']["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.add_members['logging']["file_name"], maxBytes=config.add_members['logging']["max_bytes"], backupCount=config.add_members['logging']["back_up_count"])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"], config.environment["password"])
    xm_collection = xmatters.xMattersCollection(environment)
    xm_person = xmatters.xMattersPerson(environment)
    xm_shift = xmatters.xMattersShift(environment)
    xm_group = xmatters.xMattersGroup(environment)
    members_file = xmatters.Column(config.add_members['file']["file_name"], config.add_members['file']["encoding"])

    # execute the main process
    main()

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))
