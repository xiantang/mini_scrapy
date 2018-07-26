



class Crawler():

    def __init__(self,spider_cls,*args,**kwargs):
        self.spider_cls = spider_cls
        self._load_spider()
        self.spider = None
        self._load_spider(*args,**kwargs)



    def _load_spider(self,*args,**kwargs):
        spider=self.spider_cls.from_crawler(self,*args,**kwargs)
        self.spider=spider


    def exec(self):
        self.spider.start()