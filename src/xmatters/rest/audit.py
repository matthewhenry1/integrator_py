# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersAudit(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_audit(self, url_filter=""):
        def_name = "get_audit "
        try:
            self.__log.debug(def_name + "Getting Events with Filter: " + url_filter)
            response = self.__request.get("/api/xm/1/audits?" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response
