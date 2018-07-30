from queue import Queue

from mini_scrapy.dupefilters import RFPDupeFilter
from mini_scrapy.untils.untils import logger


class Scheduler(object):
    """ Scheduler """

    def __init__(self,settings,filter,queue,):
        # self.request_filter = RFPDupeFilter()
        # self.queue = Queue()
        self.settings = settings
        self.request_filter = filter
        self.queue = queue

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        request_filter = RFPDupeFilter()
        queue = Queue()
        return cls(settings,request_filter,queue)


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
