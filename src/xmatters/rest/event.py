# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersEvent(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_events(self, filter_url=""):
        def_name = "get_events "
        try:
            self.__log.debug(def_name + "Getting Events with Filter: " + filter_url)
            response = self.__request.get("/api/xm/1/events?" + filter_url)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_an_event(self, event_id, filter_url=""):
        def_name = "get_an_event "
        try:
            self.__log.debug(def_name + "Getting Groups")
            response = self.__request.get("/api/xm/1/events/" + event_id + "/" + filter_url)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_user_deliveries(self, event_id, filter_url=""):
        def_name = "get_user_deliveries "
        try:

            self.__log.debug(def_name + " Getting User Deliveries ")
            response = self.__request.get("/api/xm/1/events/" + event_id + "/user-deliveries?" + filter_url)

            response_data = {
                "data": response['data']
            }

            self.__log.info('initial event data - ' + json.dumps(response_data))

            count = int(response['count'])

            self.__log.info('Count: ' + str(count) + ' Total: ' + str(response['total']))

            if self.__has_next_link(response):
                next_link = response["links"]["next"]
                self.__log.info('Has next link')
            else:
                next_link = False

            # if obj, will loop
            while next_link:
                response = self.__request.get(next_link)

                count = int(response['count']) + count
                self.__log.info('Next Link: ' + str(next_link))
                self.__log.info('Count: ' + str(count) + ' Total: ' + str(response['total']))

                if response:
                    for item in response["data"]:
                        response_data['data'].append(item)

                    if self.__has_next_link(response):
                        next_link = response["links"]["next"]
                    else:
                        next_link = False
                else:
                    next_link = False

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response_data

    def __has_next_link(self, obj):
        has = True
        try:
            # an exception will throw if it doesn't exist
            obj["links"]["next"]
        except:
            has = False
        return has