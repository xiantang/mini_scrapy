from queue import LifoQueue, Queue
from mini_scrapy.untils.untils import logger, load_objects


class Scheduler(object):
    """
        Scheduler
        控制url进出队列/过滤url的操作
        控制item/进出队列的操作
    """

    def __init__(self, crawler, settings, filter):
        # self.request_filter = RFPDupeFilter()
        # self.queue = Queue()
        # TODO:自己造一个queue的轮子
        self.settings = settings
        self.request_filter = filter
        self.request_queue = LifoQueue()
        self.crawler = crawler
        self.item_queue = Queue()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        filter_cls = load_objects(settings['DUPEFILTER'])
        request_filter = filter_cls.from_crawler(crawler)
        return cls(crawler, settings, request_filter)

    def enqueue_request(self, request):
        """put request
        如果没有不过滤 /request_seen 看到了就过滤
        """
        if request.meta["retry_count"] >0:
            self.request_queue.put(request)
        elif not request.dont_filter \
                and self.request_filter.request_seen(request):
            logger.warn("ignore %s", request.url)
            return
        else:
            self.request_queue.put(request)

    def next_request(self):
        """
        next request
        :return:
        """
        if self.request_queue.empty():
            return None
        next_request = self.request_queue.get()
        self.request_queue.task_done()
        return next_request

    def is_empty(self):
        """
        判断是否为空
        :return:
        """

    def enqueue_item(self,item,spider):
        """
        将item放入队列
        :param item:
        :param spider:
        :return:
        """
        self.item_queue.put(item)

    def __len__(self):
        return self.request_queue.qsize()
