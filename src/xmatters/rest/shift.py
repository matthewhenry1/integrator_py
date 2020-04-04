import logging
import urllib.parse
from .api import xMattersAPI
import json


class xMattersShift(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def add_member_to_shift(self, group_id, shift_id, member_id):
        def_name = "add_member_to_shift "
        try:
            self.__log.debug(def_name + "adding member " + member_id + " to group " + group_id + " shift " + shift_id)
            data = {
                "recipient": {
                    "id": str(member_id),
                    "recipientType": "PERSON"
                }
            }

            response = self.__request.post(data, "/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/shifts/" + urllib.parse.quote(shift_id, safe='') + "/members")

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_shift(self, group_id, shift_id):
        def_name = "get_shift "
        try:
            self.__log.debug(def_name + "Getting Group: " + group_id)
            response = self.__request.get("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/shifts/" + urllib.parse.quote(shift_id, safe=''))

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_shifts(self, group_id):
        def_name = "get_shifts "
        try:
            self.__log.debug(def_name + "Getting Group Shifts: " + group_id)
            response = self.__request.get("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/shifts")

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def create_shift(self, group_id, data):
        def_name = "create_shift "
        try:
            self.__log.debug(def_name + "Creating Shift, for " + group_id)
            response = self.__request.post(data, "/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/shifts")

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def delete_shift(self, group_id, shift_id):
        def_name = "delete_shift "
        try:
            self.__log.debug(def_name + "Getting Group: " + group_id)
            response = self.__request.delete("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/shifts/" + urllib.parse.quote(shift_id, safe=''))

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response
