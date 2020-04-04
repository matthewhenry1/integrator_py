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


class xMattersCollection(xMattersCollectionThread):

    # constructor
    def __init__(self, *args, **kwargs):
        super(xMattersCollection, self).__init__(*args, **kwargs)
        self.response = []
        self.errors = []

    def create_collection(self, child_method, data, thread_count):
        del self.response[:]  # first clear the list from any previous processes
        del self.errors[:]

        self.create_thread_collection(child_method, data, thread_count, self.execute)
        return {"response": self.response, "errors": self.errors}

    def execute(self, method, thread, data):
        for i in range(len(data)):
            self.log.debug(
                "Thread number: " + str(thread) + " Executing Method: " + str(method) + " with Incoming data: " + str(
                    data[i]))

            signature = inspect.signature(method)
            params = {}
            for param in signature.parameters:
                if param in data[i]:
                    params[param] = data[i][param]
            self.log.debug(
                "Thread number: " + str(thread) + "Executing Method: " + str(method) + " with Param Data: " + str(
                    params))

            response = method(**params)
            if response:
                self.response.append({"request_body": data[i], "response_body": response})
            else:
                self.errors.append(data[i])
