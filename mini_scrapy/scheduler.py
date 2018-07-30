from queue import Queue

from mini_scrapy.utils import logger, request_fingerprint
from mini_scrapy.bloom import BloomFilter

class Scheduler(object):

    """ Scheduler """

    def __init__(self):
        self.request_filter = RequestFilter()
        self.queue = Queue()

    def enqueue_request(self, request):
        """put request
        """
        if not request.dont_filter \
                and self.request_filter.request_seen(request):
            logger.warn("ignore %s", request.url)
            return
        self.queue.put(request)

    def next_request(self):
        """
        next request
        :return:
        """
        if self.queue.empty():
            return None
        next_request = self.queue.get()
        self.queue.task_done()
        return next_request

    def __len__(self):
        return self.queue.qsize()


class RequestFilter(object):

    def __init__(self):
        #TODO read arg from setting
        self.sbf = BloomFilter(
            100000,10
        )

    def request_seen(self,request):
        """
        request seen
        :param requests:
        :return:
        """

        finger = request_fingerprint(request)
        if finger in self.sbf:
            return True
        self.sbf.add(finger)
        return False