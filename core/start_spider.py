from mini_scrapy.core.crawler import Crawler

def run(spidercls):
    crawler=init_spider(spidercls=spidercls)
    crawler.exec()

def init_spider(spidercls):
    c=Crawler(spidercls)
    return c