import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
import json
import ssl
import time
import logging


def status_code_success(status_code):
    return 200 <= status_code <= 299


def too_many_requests(status_code):
    if status_code == 429:
        time.sleep(10)
        return True
    else:
        return False


def gateway_time_out(status_code):
    if status_code == 504:
        return True
    else:
        return False


def has_response_body(response):
    try:
        json_str = response.json()
    except:
        json_str = None
    return json_str


class xMattersAPI(object):

    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__log = logging.getLogger(__name__)
        self.__max_retry = 3

    def execute(self, function, *args, **kwargs):
        retry = 0
        json_str = None
        while retry < self.__max_retry:
            try:
                response = function(*args, **kwargs)
                if status_code_success(response.status_code):
                    json_str = has_response_body(response)
                    if json_str:
                        self.__log.debug(
                            "Received Status Code: " + str(response.status_code) + " and Response Body: " + json.dumps(
                                json_str))
                    else:
                        self.__log.debug(
                            "Received Status Code: " + str(response.status_code) + " and Response Body: " + str(
                                json_str))
                    break
                elif too_many_requests(response.status_code):
                    self.__log.error("Status Code: " + str(response.status_code) + ". Too many requests. Retrying request, retry count: " + str(retry))
                    retry = retry + 1
                    json_str = None
                    continue
                elif gateway_time_out(response.status_code):
                    self.__log.error(
                        "Status Code: " + str(response.status_code) + " and Response Body: " + str(response.content) +
                        ". Retrying request, retry count: " + str(retry))
                    retry = retry + 1
                    json_str = None
                    continue
                else:
                    self.__log.debug(
                        "Received Status Code: " + str(response.status_code) + " and Response Body: " + str(
                            response.content))
                    json_str = None
                    break
            except Exception as e:
                self.__log.error("Unexpected exception:" + str(e))
                json_str = None
                break

        return json_str

    def post(self, data, path, headers=None):
        return self.execute(requests.post, self.__url + path, auth=HTTPBasicAuth(self.__username, self.__password),
                            headers={"Content-Type": "application/json"} if not headers else headers,
                            data=json.dumps(data))

    def put(self, data, path, headers=None):
        return self.execute(requests.put, self.__url + path, auth=HTTPBasicAuth(self.__username, self.__password),
                            headers={"Content-Type": "application/json"} if not headers else headers,
                            data=json.dumps(data))

    def get(self, path):
        return self.execute(requests.get, self.__url + path, auth=HTTPBasicAuth(self.__username, self.__password))

    def delete(self, path):
        return self.execute(requests.delete, self.__url + path, auth=HTTPBasicAuth(self.__username, self.__password))
