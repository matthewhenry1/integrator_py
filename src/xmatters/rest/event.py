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

    def get_events(self, url_filter=""):
        def_name = "get_events "
        try:
            self.__log.debug(def_name + "Getting Events with Filter: " + url_filter)
            response = self.__request.get("/api/xm/1/events?" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_an_event(self, event_id, url_filter=""):
        def_name = "get_an_event "
        try:
            self.__log.debug(def_name + "Getting Groups")
            response = self.__request.get("/api/xm/1/events/" + event_id + "/" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_user_deliveries(self, event_id, url_filter=""):
        def_name = "get_user_deliveries "
        try:

            self.__log.debug(def_name + " Getting User Deliveries ")
            response = self.__request.get("/api/xm/1/events/" + event_id + "/user-deliveries?" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def __has_next_link(self, obj):
        has = True
        try:
            # an exception will throw if it doesn't exist
            obj["links"]["next"]
        except:
            has = False
        return has

