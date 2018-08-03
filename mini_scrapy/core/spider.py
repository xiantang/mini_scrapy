"""Base Spider"""

from mini_scrapy.http.request import Request
from mini_scrapy.untils.untils import logger


class Spider(object):
    """
    Base Spider
    """
    name = None
    custom_setting = {}

    def __init__(self,crawler, name=None, **kwargs):
        """初始化爬虫"""
        self._set_crawler(crawler)
        if name is not None:
            self.name = name
        if not hasattr(self, "start_urls"):
            self.start_urls = []
            # 初始化

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler,*args, **kwargs)

        return spider

    def _set_crawler(self, crawler):
        self.crawler = crawler
        self._load_settings()

    def _load_settings(self):
        """
        load setings of custom_setting and settings.py
        :return:
        """

        self.settings = self.crawler.settings
        self.settings.set_dict(self.custom_setting)
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        raise NotImplementedError

    # def process_item(self, item):
    #     logger.info("Process_item:\n \t {item}".format(item=item))
        # pass
