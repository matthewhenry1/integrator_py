# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI

class xMattersOnCall(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_on_call_collection(self, url_filter=""):

        def_name = "get_on_call_collection "
        try:
            url_filter = self.__parse_filter(url_filter)
            self.__log.debug(def_name + "Getting OnCall Collection, with filter: " + url_filter)

            groups = self.__get_on_call_groups("?offset=0&limit=1000&membersPerShift=100" + url_filter)

            if not groups:
                self.__log.debug(def_name + "OnCall Not Retrieved")
                return None

            total = groups["total"]
            count = groups["count"]
            p = 0
            oncall = []

            while p < total:
                for item in groups["data"]:

                    if self.__has_next_link(item["members"]):
                        continue_to_get_members = True
                        member_link = None
                        while continue_to_get_members:

                            if not member_link:  #  only execute below on first iteration
                                members = self.__get_on_call_members(item["members"]["links"]["next"])
                            else:  # for all other iterations
                                members = self.__get_on_call_members(member_link)

                            if members:  # only execute if there are members to process
                                for member in members["data"]:
                                    item["members"]["data"].append(member)

                                # get next series
                                if self.__has_next_link(members):
                                    member_link = members["links"]["next"]
                                else:
                                    continue_to_get_members = False
                            else:
                                continue_to_get_members = False

                    # let"s clear the links
                    item["members"].pop("links", None)
                    oncall.append(item)

                # increment the pagination count
                p = p + count

                if p < total:
                    groups = self.__get_on_call_groups("?offset="+str(p)+"&limit=1000"+url_filter)
                    count = groups["count"]

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception: " + str(e))
            oncall = []

        self.__log.debug(def_name + "Returning OnCall: " + json.dumps(oncall))

        return oncall
    
    # private method
    def __get_on_call_groups(self, url_filter="?offset=0&limit=1000"):

        def_name = "__get_on_call_groups "

        try:
            self.__log.debug(def_name + "Getting OnCall for Groups")
            response = self.__request.get("/api/xm/1/on-call" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    # private method
    def __get_on_call_members(self, url_filter):

        def_name = "__get_on_call_members "

        try:
            self.__log.debug(def_name + "Getting OnCall for Members")
            response = self.__request.get(url_filter)
        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    # private method
    # purpose of this filter is to remove membersPerShift, offset, and limit
    def __parse_filter(self, url_filter=""):
        def_name = "__parse_filter "
        new_filter = ""

        try:
            for filter_str in url_filter.split("&"):
                if filter_str == "":
                    new_filter = new_filter + filter_str
                else:
                    if filter_str.find("membersPerShift") == -1 and filter_str.find("offset") == -1 and filter_str.find("limit") == -1:
                        new_filter = new_filter + "&" + filter_str
        except Exception as e:
            self.__log.error(def_name + "Unexpected exception: " + str(e))

        return new_filter

    def __has_next_link(self, obj):
        has = True
        try:
            # an exception will throw if it doesn't exist
            obj["links"]["next"]
        except:
            has = False
        return has