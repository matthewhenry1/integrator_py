# local imports
import xmatters
import config

# python3 package imports
import logging
import json
from logging.handlers import RotatingFileHandler


# main process
def main() -> object:

    """the main process that can be leveraged for calling other modules to intitiate procesess, etc. below are examples of the xMatters REST API with pyxmatters"""

    """xMattersPerson Examples:"""
    # for i in range(50):
    #     xm_person.create_person({'targetName': 'new_target_' + str(i), 'firstName': 'new_target_' + str(i), 'lastName': 'new_target_' + str(i),
    #          'roles': ['Group Supervisor']})
    # xm_person.get_person('atarget_0')
    # xm_person.get_people_collection()
    # xm_person.remove_person('atarget_1')

    """xMattersDevice Examples:"""
    # user_id = xm_person.get_person('atarget_3')['id'] # needed for device creation
    # xm_device.create_device({'name': 'Work Email', 'emailAddress': 'user@xmatters.com', 'deviceType': 'EMAIL', 'owner': user_id})
    # xm_device.get_devices()

    """xMattersGroup Examples:"""
    # group = xm_group.create_group({'targetName': 'Test Group'})
    # xm_group.modify_group({'id': group['id'], 'status': 'INACTIVE'})
    # xm_group.get_group('Test Group')
    # xm_group.get_group_collection()
    # xm_group.remove_group('Test Group')

    """xMattersRoster Examples:"""
    # xm_roster.add_member_to_roster('Test Group', 'atarget_10')
    # xm_roster.get_roster('Test Group')
    # xm_roster.remove_member_from_roster('Test Group', 'TestUser')

    """xMattersShift Examples:"""
    # xm_shift.create_shift('Test Group', {'name': 'Test Shift'})
    # xm_shift.add_member_to_shift('Test Group', 'Default Shift', 'atarget_10')
    # xm_shift.get_shifts('Test Group')
    # xm_shift.get_shift('Test Group', 'Default Shift')
    # xm_shift.delete_shift('Test Group', 'Default Shift')

    """xMattersSite Examples:"""
    # xm_site.create_site({'name': 'New Site', 'timezone': 'US/Eastern', 'language': 'EN', 'country': 'USA'})
    # site = xm_site.get_site('Default Site')
    # xm_site.get_sites()
    # xm_site.modify_site({'id': site['id'], 'timezone': 'US/Pacific'})


# entry point when file initiated
if __name__ == "__main__":
    # configure the logging
    logging.basicConfig(level=config.logging["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.logging["file_name"], maxBytes=config.logging["max_bytes"],
                                                      backupCount=config.logging["back_up_count"])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"], config.environment["password"])
    xm_person = xmatters.xMattersPerson(environment)
    xm_device = xmatters.xMattersDevice(environment)
    xm_group = xmatters.xMattersGroup(environment)
    xm_collection = xmatters.xMattersCollection(environment)
    xm_roster = xmatters.xMattersRoster(environment)
    xm_shift = xmatters.xMattersShift(environment)
    xm_site = xmatters.xMattersSite(environment)
    xm_on_call = xmatters.xMattersOnCall(environment)

    # execute the main process
    main()

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))
