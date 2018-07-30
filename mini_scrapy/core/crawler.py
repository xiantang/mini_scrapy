import importlib

from mini_scrapy.conf.settings import Settings
from mini_scrapy.core.engine import Engine


class Crawler():

    def __init__(self, spider_cls, *args, **kwargs):
        self._load_settings()
        self.spider_cls = spider_cls
        self.spider = None
        self.engine = None
        self.spider = self._create_spider(*args, **kwargs)
        self.engine = self._create_engine()

    def _create_spider(self, *args, **kwargs):
        spider = self.spider_cls.from_crawler(self, *args, **kwargs)
        return spider

    def _create_engine(self):
        engine = Engine(self)
        return engine

    def _load_settings(self):
        #用户自定义的settings
        custom_settings = importlib.import_module('settings')
        #加载default_settings
        self.settings = Settings()
        self.settings.load_config(custom_settings)

    def exec(self):
        self.engine.start()
