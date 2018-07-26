"""Base Spider"""

from http_client.request import Request
from core.Engine import Engine
from conf.settings import Settings

class Spider(object):
    """
    Base Spider
    """
    name =None
    custom_setting = None

    def __init__(self,name=None,**kwargs):
        """初始化爬虫"""
        if name is not None:
            self.name=name
        if not hasattr(self,"start_urls"):
            self.start_urls = []
            #初始化
        self.settings = Settings(self.custom_setting)
        self.initialize()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider.crawler = spider._set_crawler(crawler)
        return spider

    def _set_crawler(self,crawler):
        self.crawler = crawler

    def initialize(self):
        """
        initialize
        :return:
        """
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def start(self):
        engine = Engine(self)
        engine.start()

    def parse(self,response):
        raise NotImplementedError

    def process_item(self,item):
        pass

if __name__ == '__main__':
    s = Spider()
    s.start()