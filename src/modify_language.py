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
    """
        Background:
        1. Query for users in xM based on property name/value search criteria
        2. Push results to an array
        3. Based on array inspect data and build payload
        4. With payload update xMatters
    """

    # captures the results of the search
    people = []

    # first loop through the properties object for the property name
    for prop_name in config.modify_language['properties']:

        # next loop through the values associated to the individual property
        for prop_val in config.modify_language['properties'][prop_name]:
            # build param string
            param_data = {
                "url_filter": '?'+urllib.parse.quote(prop_name, safe='')+'=' + urllib.parse.quote(prop_val, safe=''),
            }

            # get initial page
            people_search = xm_person.get_people(param_data['url_filter'] + '&offset=0&limit=' + str(config.modify_language['page_size']))

            # if nothing is returned let's skip this search loop
            if not people_search:
                log.info('No users found from the instance for search: ' + str(param_data['url_filter']))
                continue

            # if the total returned from the the search is greater than the config page size, then we have more searching to do
            if people_search['total'] > config.modify_language['page_size']:
                people_collection = xm_collection.get_collection(xm_person.get_people, people['total'],
                                                                 config.modify_language['page_size'], param_data,
                                                                 config.modify_language['thread_count'])

                # log and then concat two arrays
                log.info("Retrieved " + str(len(people_collection['response'])) + " people from search: " + str(param_data['url_filter']))
                people = people_collection['response'] + people
            else:
                # else, continue on with that initial request and concat the two arrays
                log.info("Retrieved " + str(len(people_search['data'])) + " people from search: " + str(param_data['url_filter']))
                people = people_search['data'] + people

    log.debug('Retrieved people data: ' + json.dumps(people))
    log.info('Retrieved people count: ' + str(len(people)))

    # now let's iterate through, build the payload, and make sure we're only updating users that are ACTIVE
    request_data = []
    for data in people:
        try:
            if data['language'] != "pt_BR":
                request_data.append(dict(data=dict(targetName=data['targetName'],
                                         id=data['id'],
                                         language="pt_BR")))
        except Exception as e:
            log.error('Exception ' + str(e) + ' on line:  ' + str(data))

    log.info('Number of requests for update: ' + str(len(request_data)))
    log.info('Requests for update: ' + json.dumps(request_data))

    # # only execute if there are requests
    if len(request_data) > 0:
        person_response = xm_collection.create_collection(xm_person.modify_person, request_data, config.modify_language['thread_count'])
        log.info("Update response: " + str(person_response["response"]))
        log.info("Update errors: " + str(person_response["errors"]))


if __name__ == "__main__":
    # configure the logging
    logging.basicConfig(level=config.modify_language['logging']["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.modify_language['logging']["file_name"],
                                                      maxBytes=config.modify_language['logging']["max_bytes"],
                                                      backupCount=config.modify_language['logging']['back_up_count'])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"],
                                       config.environment["password"])
    xm_person = xmatters.xMattersPerson(environment)
    xm_collection = xmatters.xMattersCollection(environment)

    main()  # execute the main process

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))
