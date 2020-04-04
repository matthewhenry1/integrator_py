# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersDevice(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_device(self, device_id, url_filter="?embed=timeframes"):
        def_name = "get_device "
        try:
            self.__log.debug(def_name + "Getting Device: " + device_id)
            response = self.__request.get("/api/xm/1/devices/" + urllib.parse.quote(device_id, safe='') + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_devices(self, url_filter="?embed=timeframes"):
        def_name = "get_devices "
        try:
            self.__log.debug(def_name + "Getting Devices")
            response = self.__request.get("/api/xm/1/devices" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def create_device(self, data):
        def_name = "create_device "
        try:
            self.__log.debug(def_name + "Creating Device: " + data["name"] + " for owner: " + data["owner"])
            response = self.__request.post(data, "/api/xm/1/devices")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def modify_device(self, data):
        def_name = "modify_device "
        try:
            self.__log.debug(def_name + "Modifying Devices: " + data["id"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/devices/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e) + " with data: " + str(data))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def remove_device(self, device_id):
        def_name = "remove_device "
        try:
            self.__log.debug(def_name + "Removing Device: " + device_id)
            response = self.__request.delete("/api/xm/1/devices/" + device_id)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response
