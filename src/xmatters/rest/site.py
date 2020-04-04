# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersSite(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_site(self, site_id):
        def_name = "get_site "
        try:
            self.__log.debug(def_name + "Getting Site: " + site_id)
            response = self.__request.get("/api/xm/1/sites/" + urllib.parse.quote(site_id, safe=''))

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def create_site(self, data):
        def_name = "create_site "
        try:
            self.__log.debug(def_name + "Creating Site: " + data["name"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/sites/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_sites(self):
        def_name = "get_sites "
        try:
            self.__log.debug(def_name + "Getting Sites")
            response = self.__request.get("/api/xm/1/sites")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def modify_site(self, data):
        def_name = "modify_site "
        try:
            self.__log.debug(def_name + "Modifying Site: " + data["id"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/sites/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response
