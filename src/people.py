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
        1. Query for users in an instance and push to an array
        2. Write to a CSV
    """
    current_date_time = datetime.datetime.now()
    people = xm_person.get_people('?offset=0&limit='+str(config.people['page_size']))

    if not people:
        log.info('No users found from the instance')
        return

    # if above the page size limit execute the collection
    if people['total'] > config.people['page_size']:
        param_data = {
            "url_filter": '?embed=roles,devices',
        }
        people_collection = xm_collection.get_collection(xm_person.get_people, people['total'], config.people['page_size'], param_data, config.people['thread_count'])
        people = people_collection['response']
    else:  # otherwise continue on with that initial request
        people = people['data']

    log.debug('Retrieved people data: ' + json.dumps(people))
    log.info('Retrieved people count: ' + str(len(people)))

    csv_data = []
    for data in people:
        try:
            if hasattr(data['properties'], 'Emp Status'):
                if data['properties']['Emp Status'] != 'L' or data['properties']['Emp Status'] != 'P':
                    csv_data.append(dict(targetName=data['targetName'],
                                         retrieved_date_time=str(current_date_time.isoformat())))
                else:
                    log.debug('Not adding, User: ' + data['targetName'] + ' has Emp Status of ' + data['properties']['Emp Status'])
            else:
                csv_data.append(dict(targetName=data['targetName'],
                                     retrieved_date_time=str(current_date_time.isoformat())))
        except Exception as e:
            log.error('Exception ' + str(e) + ' on line:  ' + str(data))

    log.info('Found Number of Rows for People: ' + str(len(csv_data)))

    if len(csv_data) > 0:
        with open(config.people['file_name'], 'w', newline='', encoding=config.people['encoding']) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            # write the header
            csv_writer.writerow(['targetName', 'retrieved_date_time'])

            # write the values
            for row in csv_data:
                csv_writer.writerow([row['targetName'], row['retrieved_date_time']])

if __name__ == "__main__":
    # configure the logging
    logging.basicConfig(level=config.people['logging']["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.people['logging']["file_name"], maxBytes=config.people['logging']["max_bytes"],
                                                      backupCount=config.people['logging']['back_up_count'])])
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
