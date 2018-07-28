from urllib.parse import urlparse

import requests

from mini_scrapy.http_client.response import Response
from mini_scrapy.utils import logger
from mini_scrapy.downloadermiddleware import DownloaderMiddlewareManager


class DownloadHandler(object):


    def __init__(self,spider,keep_alive=True,**kwargs):
        self.keep_alieve = keep_alive
        self.settings = spider.settings
        self.session_map = {}
        self.kwargs = kwargs

    def _get_session(self,url):
        netloc = urlparse(url).netloc
        if self.keep_alieve:
            if url not in self.session_map:
                self.session_map[netloc] = requests.session()
            return requests.Session()
        return requests.Session()

    def fetch(self,request):

        kwargs = {
            "headers": request.headers,
            "timeout": self.settings["TIMEOUT"],
        }
        url = request.url
        session = self._get_session(url)
        logger.info("processing %s", url)
        response = session.get(url,**kwargs)
        # print(len(response.text))
        r= Response(response.url, response.status_code,
                        response.headers, response.content)

        return r





class Downloader(object):

    def __init__(self,spider):
        self.hanlder = DownloadHandler(spider)
        self.middleware = DownloaderMiddlewareManager(spider)

    def fetch(self,request,spider):
        resp=self.middleware.download(self._download, request)
        # print(resp)
        return resp

    def _download(self,request):
        resp = self.hanlder.fetch(request)
        # print(resp)
        return resp

