from queue import Queue
from mini_scrapy.untils.untils import logger, load_objects


class Scheduler(object):
    """ Scheduler """

    def __init__(self, crawler, settings, filter):
        # self.request_filter = RFPDupeFilter()
        # self.queue = Queue()
        # TODO:自己造一个queue的轮子
        self.settings = settings
        self.request_filter = filter
        self.queue = Queue()
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        filter_cls = load_objects(settings['DUPEFILTER'])
        request_filter = filter_cls.from_crawler(crawler)
        return cls(crawler, settings, request_filter)

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

    def is_empty(self):
        """
        判断是否为空
        :return:
        """

    def __len__(self):
        return self.queue.qsize()
