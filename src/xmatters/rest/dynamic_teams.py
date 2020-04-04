# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersDynamicTeams(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def create_dynamic_team(self, data):
        def_name = "create_dynamic_team "
        try:
            self.__log.debug(def_name + "Creating Dynamic Team: " + data["targetName"] + " with " + json.dumps(data))
            response = self.__request.post(data, "/api/xm/1/dynamic-teams/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response
