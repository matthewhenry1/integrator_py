# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersPlans(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_plan(self, plan_id, url_filter="?embed=creator,constants,endpoints,forms,propertyDefinitions,integrations"):
        def_name = "get_plan "
        try:
            self.__log.debug(def_name + "Getting Plan: " + plan_id)
            response = self.__request.get("/api/xm/1/plans/" + urllib.parse.quote(plan_id, safe='') + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response
