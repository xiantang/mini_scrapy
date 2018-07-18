from urllib.parse import urlparse

import requests

from http_.response import Response
from utils import logger


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
        return Response(response.url,response.s)


class Downloader(object):

    def __init__(self,spider):
        self.hanlder = DownloadHandler(spider)
        self.middleware = DownloaderMiddlewareManger(spider)

    def fetch(self,request,spider):
        return self.middleware.download(self._download,request)

    def _download(self,request):
        return self.hanlder.fetch(request)

