"""Base Spider"""

from mini_scrapy.http.request import Request
from mini_scrapy.core.engine import Engine
from mini_scrapy.conf.settings import Settings


class Spider(object):
    """
    Base Spider
    """
    name = None
    custom_setting = None

    def __init__(self, name=None, **kwargs):
        """初始化爬虫"""
        if name is not None:
            self.name = name
        if not hasattr(self, "start_urls"):
            self.start_urls = []
            # 初始化

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider.crawler = spider._set_crawler(crawler)
        return spider

    def _set_crawler(self, crawler):
        self.crawler = crawler
        self._load_settings()

    def _load_settings(self):
        """
        load setings of custom_setting and settings.py
        :return:
        """
        # TODO:load custom user defined in spider.
        self.settings = self.crawler.settings

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        raise NotImplementedError

    def process_item(self, item):
        pass
