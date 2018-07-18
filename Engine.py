from gevent import monkey
monkey.patch_all()

from utils import spawn, get_result_list, join_all

import logging
import gevent
from gevent.pool import Pool
from scheduler import Scheduler
from downloader import Downloader
from http_client.request import Request

class Engine(object):
    """
    Engine
    """

    def __init__(self,spider):
        """
        :param spider: spider obj
        """
        self.spider= spider
        self.scheduler = Scheduler()
        self.downloader = Downloader(spider)
        self.setting = spider.settings
        max_request_size = self.setting['MAX_REQUEST_SIZE']
        self.pool = Pool(size=max_request_size)

    def start(self):
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider,start_requests)

    def execute(self,spider,start_requests):
        self.start_requests = start_requests
        all_routines = []
        all_routines.append(spawn(self._init_start_requests))
        all_routines.append(spawn(self._next_request,spider))
        # all_routines.append(spawn(self._next_request,spider))
        join_all(all_routines)
    def _init_start_requests(self):
        """
        init start requests
        :return:
        """
        for req in  self.start_requests:
            # print(req)
            self.crawl(req)

    def _next_request(self,spider):
        while 1:
            request = self.scheduler.next_request()
            #从调度器中取出request对象
            if not request:
                gevent.sleep(0.2)
                continue

            #拿出来下载
            self.pool.spawn(
                self._process_request,request,spider
            )

    def _process_request(self,request,spider):
        try:
            response = self.download(request,spider)
        except Exception as exc:
            logging.error("download error: %s", str(exc), exc_info=True)
        else:
            #判断是不是request对象如果是就重新压入队列
            self._handle_downloader_output(response,request,spider)
            return response

    def download(self,request,spider):
        response = self.downloader.fetch(request,spider)
        response.request = request
        return response


    def crawl(self,request):
        """
        把request 压进队列
        :param request:
        :return:
        """
        self.scheduler.enqueue_request(request)

    def _handle_downloader_output(self,response,request,spider):
        if isinstance(response,Request):
            self.crawl(response)
            return
        self.process_response(response,request,spider)

    def process_response(self,response, request, spider):
        """

        :param response:
        :param request:
        :param spider:
        :return:
        """
        callback = request.callback or spider.parse
        result = callback(response)
        ret = get_result_list(result)
        self.handle_spider_output(ret,spider)
        #去遍历result

    def handle_spider_output(self,result,spider):
        """
        解决了疑惑 可以根据yield返回的类型进行判断
        :param result:
        :param spider:
        :return:
        """
        for item in result:
            if item is None:
                continue
            elif isinstance(item,Request):
                self.crawl(item)
            elif isinstance(item,dict):
                self.process_item(item,spider)
            else:
                logging.error("Spider must retrun Request, dict or None")

    def process_item(self,item,spider):
        spider.process_item(item)

    # def _next_request(self,spider):
