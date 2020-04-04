import logging
import urllib.parse
from .api import xMattersAPI
import json


class xMattersRoster(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    # group_id = (id) or name (targetName) of the group.
    def add_member_to_roster(self, group_id, member_id):
        def_name = "add_member_to_roster "
        try:

            data = {
                "id": str(member_id),
                "recipientType": "PERSON"
            }

            response = self.__request.post(data, "/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/members")

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    # group_id = (id) or name (targetName) of the group.
    def remove_member_from_roster(self, group_id, member_id):
        def_name = "remove_member_from_roster "
        try:
            self.__log.debug(def_name + "removing member "+member_id+" from group roster " + group_id)
            response = self.__request.delete("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/members/"+urllib.parse.quote(member_id, safe=''))

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    # group_id = (id) or name (targetName) of the group.

    def get_roster(self, group_id, url_filter="&offset=0&limit=1000"):
        def_name = "get_roster "
        try:
            self.__log.debug(def_name + "Getting Group Roster: " + group_id)
            response = self.__request.get("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + "/members?embed=shifts" +url_filter)

        except Exception as e:
            self.__log.error(
                def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    # group_id = (id) or name (targetName) of the group.
    def get_roster_collection(self, group_id):
        def_name = "get_roster_collection "
        try:
            self.__log.debug(def_name + "Getting Group Roster Collection: " + group_id)
            roster = self.get_roster(group_id, "&offset=0&limit=1000")

            if not roster:
                self.__log.debug(def_name + "Group Not Retrieved: " + group_id)
                return None

            total = roster["total"]
            count = roster["count"]
            p = 0
            members = set()

            while p < total:
                for item in roster["data"]:
                    members.add(item["member"]["targetName"])

                # increment the pagination count
                p = p + count

                if p < total:
                    roster = self.get_roster(group_id, "&offset="+str(p)+"&limit=1000")
                    count = roster["count"]

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            members = set()

        self.__log.debug(def_name + "Returning members: " + str(members))

        return members
