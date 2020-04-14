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
        1. Query for all events related to a form and push it to an array
        2. Query for audits of each individual event and push it to an array
        3. Write to a CSV

    """

    today_date = str(datetime.date.today().isoformat())
    # today_date = '2020-04-04'  # uncomment to override above to a past date stamp
    log.info(today_date)

    events = xm_event.get_events(
        'form=' + urllib.parse.quote(config.responses['form'], safe='') + '&from=' + today_date +
        urllib.parse.quote('T00:00:00.000Z', safe=''))

    log.info('Received events ' + json.dumps(events))

    log.info('Getting User Deliveries for ' + str(len(events['data'])))
    current_date_time = datetime.datetime.now()

    csv_data = []
    for event in events['data']:

        event_user_delivery = xm_event.get_user_deliveries(event['id'], 'at=' + str(
            current_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')) + '&offset=0&limit='+str(config.responses['page_size']))

        if not event_user_delivery:
            log.info('No log data found for event id ' + event['eventId'] + ' moving to next event id.')
            continue

        # if above the page size limit execute the collection
        if event_user_delivery['total'] > config.responses['page_size']:
            param_data = {
                "url_filter": 'at=' + str(current_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')),
                "event_id": event['id']
            }
            event_user_delivery_collection = xm_collection.get_collection(xm_event.get_user_deliveries, event_user_delivery['total'], config.responses['page_size'], param_data, config.responses['thread_count'])
            event_user_delivery = event_user_delivery_collection['response']
        else:  # otherwise continue on with that initial request
            event_user_delivery = event_user_delivery['data']

        log.debug('Retrieved event_user_delivery data: ' + json.dumps(event_user_delivery))
        log.info('Retrieved event_user_delivery ' + str(len(event_user_delivery)))
        counter = 0

        for data in event_user_delivery:
            try:
                if data['deliveryStatus'] == "RESPONDED":
                    csv_data.append(dict(targetName=data['person']['targetName'],
                                         response=data['response']['text'],
                                         event_created=str(datetime.datetime.fromisoformat(
                                             event['created'].replace('+0000', "")).isoformat()),
                                         retrieved_date_time=str(current_date_time.isoformat()),
                                         delivery_status=data['deliveryStatus']))
                elif data['deliveryStatus'] == "DELIVERED":
                    csv_data.append(dict(targetName=data['person']['targetName'],
                                         response="",
                                         event_created=str(datetime.datetime.fromisoformat(
                                             event['created'].replace('+0000', "")).isoformat()),
                                         retrieved_date_time=str(current_date_time.isoformat()),
                                         delivery_status=data['deliveryStatus']))
                    counter = counter + 1
            except Exception as e:
                log.error('Exception ' + str(e) + ' on line:  ' + str(data))

        log.info('Event ID ' + event['eventId'] + ' count of user delivery data: ' + str(counter))

    log.info('Found Number of Rows for User Delivery Data: ' + str(len(csv_data)))

    if len(csv_data) > 0:
        try:
            with open(config.responses['file_name'], 'w', newline='', encoding=config.responses['encoding']) as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

                # write the header
                csv_writer.writerow(['key', 'targetName', 'response', 'event_created', 'retrieved_date_time', 'delivery_status'])

                # write the values
                for row in csv_data:
                    primary_key = row['targetName']+" "+row['event_created']
                    csv_writer.writerow([primary_key, row['targetName'], row['response'], row['event_created'], row['retrieved_date_time'], row['delivery_status']])

        except Exception as e:
            log.error('Exception while writing to csv file name: '+str(config.responses['file_name'])+' with exception: ' + str(e))

if __name__ == "__main__":
    # configure the logging
    logging.basicConfig(level=config.responses['logging']["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.responses['logging']["file_name"], maxBytes=config.responses['logging']["max_bytes"],
                                                      backupCount=config.responses['logging']['back_up_count'])])
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
