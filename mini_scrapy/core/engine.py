import sys
import time
import traceback
from threading import Thread, Event
from mini_scrapy.untils.untils import get_result_list, load_objects, logger
import logging
from mini_scrapy.http.request import Request


class Engine(object):
    """
    Engine
    """

    def __init__(self, crawler):
        """
        :param spider: spider obj
        """
        self.settings = crawler.settings
        # crawler 写死
        self.crawler = crawler
        scheduler_cls = load_objects(self.settings['SCHEDULER_PATH'])
        downloader_cls = load_objects(self.settings['DOWNLOADER_PATH'])
        self.scheduler = scheduler_cls.from_crawler(self)
        self._load_spider()
        self.downloader = downloader_cls(self.crawler)
        self.max_request_size = self.settings['MAX_REQUEST_SIZE']
        self.running = True
        # self.pool = Pool(size=max_request_size)

    def _load_spider(self):
        self.spider = self.crawler.spider

    def start(self):
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider, start_requests)

    def execute(self, spider, start_requests):
        self.start_requests = start_requests

        all_routines = []
        # daemon
        start_evt = Event()
        close_evt = Event()

        # 使主线程等待
        t_init = Thread(target=self._init_start_requests, args=(start_evt,))

        all_routines.append(t_init)

        for i in range(self.max_request_size):
            all_routines.append(Thread(target=self._next_request, args=(spider, close_evt)))

        for t in all_routines:
            t.start()

        self.close_spider(start_evt, close_evt)

    def _init_start_requests(self, start_evt):
        """
        init start requests
        :return:
        """
        logger.info("start crawling !")
        for req in self.start_requests:
            # print(req)
            self.crawl(req)
        time.sleep(1)
        start_evt.set()

    def _next_request(self, spider, close_evt):
        while not close_evt.is_set():
            request = self.scheduler.next_request()
            # 从调度器中取出request对象
            if not request:
                time.sleep(0.2)
                continue
            # 拿出来下载

            self._process_request(request, spider)

    def _process_request(self, request, spider):
        #TOdo REPLACE
        try:
            response = self.download(request, spider)
        except Exception as exc:

            logger.error("download error: %s", str(exc), exc_info=True)
        else:
            #判断是不是request对象如果是就重新压入队列
            self._handle_downloader_output(response, request, spider)
            return response

    def download(self, request, spider):
        """
        把requests的meta传入download
        :param request:
        :param spider:
        :return:
        """
        response = self.downloader.fetch(request, spider)

        response.request = request
        response.meta = request.meta
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
        exec call back func
        :param response:
        :param request:
        :param spider:
        :return:
        """
        #FIXME:集中处理异常
        callback = request.callback or spider.parse
        try:
            result = callback(response)
        except Exception as e:
            traceback_full=''.join(traceback.format_exception(*sys.exc_info()))
            logger.error(traceback_full)
            logger.error(e)
            result=[]
        #可能会导致阻塞
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
                logger.error("Spider must retrun Request, dict or None")

    def process_item(self, item, spider):
        spider.process_item(item)

    def close_spider(self, start_evt, close_evt):
        """
        关闭爬虫
        对爬虫队列不断检查
        我的思路是如果为空的话往队列里面放入flag 通过这个flag关闭线程
        :return:
        """

        # time.sleep(2)
        start_evt.wait()
        # wait 直到他set()
        while self.running:
            time.sleep(.1)
            if len(self.scheduler) == 0:
                close_evt.set()
                self.running = False
        logger.info("close spider !")

        

