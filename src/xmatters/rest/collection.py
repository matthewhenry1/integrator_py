# standard python modules
import logging
import threading
import math
import inspect
# import all local modules from the rest package
from . import *


class xMattersCollectionThread(object):

    # constructor
    def __init__(self, request):
        self.log = logging.getLogger(__name__)
        self.request = request

    def create_thread_collection(self, child_method, data, thread_count, target_method):
        bucket_size = int(math.ceil(float(len(data)) / float(thread_count)))
        threads = []
        for n in range(thread_count):
            thread_slice = data[n * int(bucket_size): (n + 1) * int(bucket_size)]
            if len(thread_slice) > 0:
                process = threading.Thread(target=target_method, args=(child_method, n, thread_slice,))
                process.start()
                threads.append(process)

        # Join all threads before proceeding
        for process in threads:
            process.join()

        return process

    def get_thread_collection(self, child_method, total, page_size, param_data, thread_count, target_method):

        # Calculate number of queries
        num_queries = int(math.ceil(float(total) / float(page_size)))
        self.log.debug('Number of Queries: ' + str(num_queries))

        # Calculate number of pages
        pages = []
        for i in range(num_queries):
            pages.append(i * page_size)
        self.log.debug("Generate pages: " + str(pages))

        # Determine bucket size
        bucket_size = int(math.ceil(float(num_queries) / float(thread_count)))
        self.log.debug("Bucket Size: " + str(bucket_size))

        threads = []
        for n in range(thread_count):
            page_slice = pages[n * int(bucket_size): (n + 1) * int(bucket_size)]

            if len(page_slice) > 0:
                self.log.debug(str(n) + '_page_slice: ' + str(page_slice))
                process = threading.Thread(target=target_method,
                                           args=(child_method, n, page_slice, page_size, param_data))
                process.start()
                threads.append(process)

        # Join all threads before proceeding
        for process in threads:
            process.join()

        return process


class xMattersCollection(xMattersCollectionThread):

    # constructor
    def __init__(self, *args, **kwargs):
        super(xMattersCollection, self).__init__(*args, **kwargs)
        self.response = []
        self.errors = []

    def create_collection(self, child_method, data, thread_count):
        del self.response[:]  # first clear the list from any previous processes
        del self.errors[:]

        self.create_thread_collection(child_method, data, thread_count, self.execute_create)
        return {"response": self.response, "errors": self.errors}

    def get_collection(self, child_method, total, page_size, param_data, thread_count):
        del self.response[:]  # first clear the list from any previous processes
        del self.errors[:]

        self.get_thread_collection(child_method, total, page_size, param_data, thread_count, self.execute_get)
        response_data = []
        for response_obj in self.response:
            for data in response_obj['response_body']['data']:
                response_data.append(data)
        return {"response": response_data, "errors": self.errors}

    def execute_create(self, method, thread, data):
        for i in range(len(data)):
            self.log.debug(
                "execute_create: Thread number: " + str(thread) + " Executing Method: " + str(
                    method) + " with Incoming data: " + str(data[i]))

            signature = inspect.signature(method)
            params = {}
            for param in signature.parameters:
                if param in data[i]:
                    params[param] = data[i][param]
            self.log.debug(
                "execute_create: Thread number: " + str(thread) + "Executing Method: " + str(
                    method) + " with Param Data: " + str(params))

            response = method(**params)
            if response:
                self.response.append({"request_body": data[i], "response_body": response})
            else:
                self.errors.append(data[i])

    def execute_get(self, method, thread, pages, page_size, param_data):
        for i in range(len(pages)):
            self.log.debug("execute_get: Thread number: " + str(thread) + " Executing Method: " + str(method) +
                          " with Incoming pages: " + str(pages[i]) + ' page_size ' + str(page_size) +
                          ' with param_data: ' + str(param_data))

            signature = inspect.signature(method)
            params = {}
            for param in signature.parameters:
                if param in param_data:
                    params[param] = param_data[param]
            self.log.debug("execute_get: Thread number: " + str(thread) + "Executing Method: " + str(method) +
                           " with Param Data: " + str(params))

            if params['url_filter']:
                params['url_filter'] = params['url_filter'] + "&offset=" + str(pages[i]) + "&limit=" + str(page_size)

            response = method(**params)
            if response:
                self.response.append({"request_body": params['url_filter'], "response_body": response})
            else:
                self.errors.append(params['url_filter'])
