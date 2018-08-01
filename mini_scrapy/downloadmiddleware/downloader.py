from urllib.parse import urlparse

import requests
from requests import Request

from mini_scrapy.http.response import Response
from mini_scrapy.untils.untils import logger
from mini_scrapy.downloadmiddleware.downloadermiddleware import DownloaderMiddlewareManager


class DownloadHandler(object):

    def __init__(self, spider, keep_alive=True, **kwargs):
        """
        如果要禁止COOKIE的话
        直接把keep_alive 设置为False
        :param spider:
        :param keep_alive:
        :param kwargs:
        """
        self.keep_alieve = keep_alive
        self.settings = spider.settings
        self.session_map = {}
        self.kwargs = kwargs

    def _get_session(self, url):
        netloc = urlparse(url).netloc
        if self.keep_alieve:
            if url not in self.session_map:
                self.session_map[netloc] = requests.session()
            return requests.Session()
        return requests.Session()



    def fetch(self, request):

        # kwargs = {
        #     "headers": request.headers,
        #     "timeout": self.settings["TIMEOUT"],
        #     "proxies":
        # }
        timeout = self.settings["TIMEOUT"]
        req = Request(
            method=request.method,
            url=request.url,
            data=request.data,
            headers=request.headers
        )
        url = request.url
        meta = request.meta
        # pre = self._get_session(url)

        session = self._get_session(url)
        prepped = session.prepare_request(req)
        logger.info("processing %s", url)
        response = session.send(prepped,
                                proxies=meta.get('proxy'),
                                timeout=timeout if meta.get("download_timeout") else timeout
                                )

        # print(len(response.text))
        r = Response(response.url, response.status_code,
                     response.headers, response.content, response.text)

        return r


class Downloader(object):

    def __init__(self, crawler):
        spider = crawler.spider
        self.hanlder = self._load_hanlder(crawler,spider)
        self.middleware = DownloaderMiddlewareManager(spider)

    def _load_hanlder(self,crawler,spider):
        is_keep_live= crawler.settings['COOKIE_ENABLE']
        hanlder=DownloadHandler(spider=spider,keep_alive=is_keep_live)
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
