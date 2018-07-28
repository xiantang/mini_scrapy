import time
from threading import Thread
from mini_scrapy.utils import get_result_list
import logging
from mini_scrapy.scheduler import Scheduler
from mini_scrapy.downloader import Downloader
from mini_scrapy.http_client.request import Request


class Engine(object):
    """
    Engine
    """

    def __init__(self, spider):
        """
        :param spider: spider obj
        """
        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader = Downloader(spider)
        self.setting = spider.settings
        self.max_request_size = self.setting['MAX_REQUEST_SIZE']
        # self.pool = Pool(size=max_request_size)

    def start(self):
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider, start_requests)

    def execute(self, spider, start_requests):
        self.start_requests = start_requests
        # TODO 完善线程池
        all_routines = []
        t_init = Thread(target=self._init_start_requests, daemon=True)

        all_routines.append(t_init)
        for i in range(self.max_request_size):
            all_routines.append(Thread(target=self._next_request, args=(spider,), daemon=True))

        for t in all_routines:
            t.start()

        self.close_spider()

    def _init_start_requests(self):
        """
        init start requests
        :return:
        """
        for req in self.start_requests:
            # print(req)
            self.crawl(req)

    def _next_request(self, spider):
        while 1:
            request = self.scheduler.next_request()
            # 从调度器中取出request对象
            if not request:
                time.sleep(0.2)
                continue

            # 拿出来下载

            self._process_request(request, spider)

    def _process_request(self, request, spider):
        try:
            response = self.download(request, spider)
        except Exception as exc:
            logging.error("download error: %s", str(exc), exc_info=True)
        else:
            # 判断是不是request对象如果是就重新压入队列
            self._handle_downloader_output(response, request, spider)
            return response

    def download(self, request, spider):
        response = self.downloader.fetch(request, spider)
        response.request = request
        return response

    def crawl(self, request):
        """
        把request 压进队列
        :param request:
        :return:
        """
        self.scheduler.enqueue_request(request)

    def _handle_downloader_output(self, response, request, spider):
        if isinstance(response, Request):
            self.crawl(response)
            return
        self.process_response(response, request, spider)

    def process_response(self, response, request, spider):
        """

        :param response:
        :param request:
        :param spider:
        :return:
        """
        callback = request.callback or spider.parse
        result = callback(response)
        ret = get_result_list(result)
        self.handle_spider_output(ret, spider)
        # 去遍历result

    def handle_spider_output(self, result, spider):
        """
        解决了疑惑 可以根据yield返回的类型进行判断
        :param result:
        :param spider:
        :return:
        """
        for item in result:
            if item is None:
                continue
            elif isinstance(item, Request):
                self.crawl(item)
            elif isinstance(item, dict):
                self.process_item(item, spider)
            else:
                logging.error("Spider must retrun Request, dict or None")

    def process_item(self, item, spider):
        spider.process_item(item)

    def close_spider(self):
        """
        关闭爬虫
        :return:
        """
        time.sleep(2)
        while True:
            if self.scheduler.queue.empty():
                logging.info("spider is over")
                break

