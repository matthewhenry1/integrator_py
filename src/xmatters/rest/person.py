# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersPerson(object):

    # constructor
    def __init__(self, request):
        self.__request = request
        self.__log = logging.getLogger(__name__)

    def get_person(self, person_id, url_filter="?embed=roles,supervisors"):
        def_name = "get_person "
        try:
            self.__log.debug(def_name + "Getting Person: " + person_id)
            response = self.__request.get("/api/xm/1/people/" + urllib.parse.quote(person_id, safe='') + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_people(self, url_filter="?embed=roles,devices&offset=0&limit=1000"):
        def_name = "get_people "
        try:
            self.__log.debug(def_name + "Getting People")
            response = self.__request.get("/api/xm/1/people" + url_filter)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def create_person(self, data):
        def_name = "create_person "
        try:
            self.__log.debug(def_name + "Creating Person: " + data["targetName"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/people/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    # Modify Person:
    #
    # data =  {
    #             "id" : "b2341d69-8b83-4660-b8c8-f2e728f675f9",
    #             "status" : "INACTIVE"
    #         }
    #
    # Reference: https://help.xmatters.com/xmapi/index.html#modify-a-person

    def modify_person(self, data):
        def_name = "modify_person "
        try:
            self.__log.debug(def_name + "Modifying Person: " + data["id"] + " with " + str(data))
            response = self.__request.post(data, "/api/xm/1/people/")

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e) + " with data: " + str(data))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def remove_person(self, person_id):
        def_name = "remove_person "
        try:
            self.__log.debug(def_name + "Removing Person: " + person_id)
            response = self.__request.delete("/api/xm/1/people/" + person_id)

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception:" + str(e))
            response = None

        self.__log.debug(def_name + "Returning response: " + str(response))

        return response

    def get_people_ids(self, supervisors):
        ids = []
        for supervisor in supervisors:
            xmsupervisor = self.get_person(supervisor)
            if xmsupervisor:
                ids.append(xmsupervisor["id"])

        return ids

    def get_people_collection(self, url_filter=''):
        def_name = "get_people_collection "
        try:
            url_filter = self.__parse_filter(url_filter)
            self.__log.debug(def_name + "Getting People Collection, with url_filter: " + url_filter)

            people = self.get_people("?offset=0&limit=1000" + url_filter)

            if not people:
                self.__log.debug(def_name + "People Not Retrieved")
                return None

            total = people["total"]
            count = people["count"]
            p = 0
            users = []

            while p < total:
                for item in people["data"]:
                    users.append(item)

                # increment the pagination count
                p = p + count

                if p < total:
                    people = self.get_people("?offset="+str(p)+"&limit=1000"+url_filter)
                    count = people["count"]

        except Exception as e:
            self.__log.error(def_name + "Unexpected exception: " + str(e))
            users = []

        self.__log.debug(def_name + "Returning users: " + json.dumps(users))

        return users

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
