from heapq import heappush
from urllib.parse import urlparse

import aiohttp
import requests
from requests import Request
from scrapy.utils.misc import load_object

from mini_scrapy.http.response import Response
from mini_scrapy.untils.untils import logger
from mini_scrapy.downloadmiddleware.downloadermiddleware import DownloaderMiddlewareManager


class DownloadHandler(object):

    def __init__(self, spider,crawler,settings,keep_alive,**kwargs):
        """
        如果要禁止COOKIE的话
        直接把keep_alive 设置为False
        :param spider:
        :param keep_alive:
        :param kwargs:
        """

        self.keep_alieve = keep_alive
        self.spider = spider
        self.crawler = crawler
        self.settings = settings
        # self.session_map = {}
        self.kwargs = kwargs

    @classmethod
    def from_crawler(cls,spider,crawler,keep_alive,**kwargs):
        settings = crawler.settings
        return  cls(spider,crawler,settings,keep_alive,**kwargs)


    def _get_session(self):
        session = aiohttp.ClientSession()
        return session
    # def _get_session(self, url):
    #     netloc = urlparse(url).netloc
    #     if self.keep_alieve:
    #         if url not in self.session_map:
    #             self.session_map[netloc] = requests.session()
    #         return requests.Session()
    #     return requests.Session()



    async def fetch(self, request):

        
        url = request.url
        meta = request.meta
        # 先不拿
        session = self._get_session()
        # response =  self.client.get(url)

        async with session.get(url) as response:
                status_code = response.status
                text = await response.text()

        r = Response(url = url, status=status_code,
                     text=text)
        session.close()
        logger.info("Downloaded ({status}) {request}".format(request=str(request),status = r.status))
        return r


class Downloader(object):

    def __init__(self, crawler):
        spider = crawler.spider
        self.hanlder = self._load_hanlder(crawler,spider)
        self.middleware = DownloaderMiddlewareManager.from_crawler(spider,crawler)

    def _load_hanlder(self,crawler,spider):
        is_keep_live= crawler.settings['COOKIE_ENABLE']
        # hanlder=DownloadHandler(spider=spider,keep_alive=is_keep_live)
        hanlder_cls = crawler.settings['DOWNLOADHANDLER_PATH']
        hanlder = load_object(hanlder_cls).from_crawler(spider,crawler,is_keep_live)
        return hanlder

    def fetch(self, request, spider):
        """

        :param request:
        :param spider:
        :return:
        """
        resp = self.middleware.download(self._download, request)

        return resp

    def _download(self, request):
        resp = self.hanlder.fetch(request)
        # if resp is None:
        #     print(1)
        # print(resp)

        return resp
