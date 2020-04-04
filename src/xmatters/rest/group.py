# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersGroup(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_group(self, group_id, url_filter="?embed=supervisors"):
        def_name = "get_group "
        try:
            self.__log.debug(def_name + "Getting Group: " + group_id)
            response = self.__request.get("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe='') + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_groups(self, url_filter="?offset=0&limit=1000"):
        def_name = "get_groups "
        try:
            self.__log.debug(def_name + "Getting Groups")
            response = self.__request.get("/api/xm/1/groups" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def create_group(self, data):
        def_name = "create_group "
        try:
            self.__log.debug(def_name + "Creating Group: " + data["targetName"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/groups/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def modify_group(self, data):
        def_name = "modify_group "
        try:
            self.__log.debug(def_name + "Modifying Group: " + data["id"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/groups/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def remove_group(self, group_id):
        def_name = "remove_group "
        try:
            self.__log.debug(def_name + "Removing Group: " + group_id)
            response = self.__request.delete("/api/xm/1/groups/" + urllib.parse.quote(group_id, safe=''))

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_group_collection(self, url_filter=''):
        def_name = "get_group_collection "
        try:
            url_filter = self.__parse_filter(url_filter)

            self.__log.debug(def_name + "Getting Groups Collection, with url_filter: " + url_filter)

            group = self.get_groups("?offset=0&limit=1000" + url_filter)

            if not group:
                self.__log.debug(def_name + "Groups Not Retrieved")
                return None

            total = group["total"]
            count = group["count"]
            p = 0
            groups = []

            while p < total:
                for item in group["data"]:
                    groups.append(item)

                # increment the pagination count
                p = p + count

                if p < total:
                    group = self.get_groups("?offset="+str(p)+"&limit=1000"+url_filter)
                    count = group["count"]

        except Exception as e:
            self.__log.error(def_name + 'Unexpected exception: ' + str(e))
            groups = []

        self.__log.debug(def_name + "Returning groups: " + json.dumps(groups))

        return groups

    def __parse_filter(self, url_filter=''):
        def_name = "__parse_filter "
        new_filter = ''
        try:
            for filter_str in url_filter.split('&'):
                if filter_str == '':
                    new_filter = new_filter + filter_str
                else:
                    if filter_str.find('offset') == -1 and filter_str.find('limit') == -1:
                        new_filter = new_filter + '&' + filter_str
        except Exception as e:
            self.__log.error(def_name + 'Unexpected exception: ' + str(e))

        return new_filter