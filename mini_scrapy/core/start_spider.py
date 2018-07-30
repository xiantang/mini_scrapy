from mini_scrapy.core.crawler import Crawler

def run(spidercls,*args,**kwargs):
    crawler=init_spider(spidercls,*args,**kwargs)
    crawler.exec()

def init_spider(spidercls,*args,**kwargs):
    c=Crawler(spidercls,*args,**kwargs)
    return c