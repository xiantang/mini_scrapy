"""
# @File  : middleware.py
# @Author: xiantang
# @Date  : 02/08/18
# @Email :zhujingdi1998@gmail.com
# blog : zhanshengpipidi.cn/blog
# Github : github.com/xiantang
"""
from mini_scrapy.downloadmiddleware.downloadermiddleware import DownloaderMiddleware

class RandomHead(DownloaderMiddleware):

    def __init__(self, spider, crawler,settings, **kwargs):
        super().__init__(spider,crawler)

    @classmethod
    def from_crawler(cls, spider, crawler, **kwargs):
        settings = crawler.settings
        return  cls(spider,crawler,settings,**kwargs)


    def process_request(self,request):
        request.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
        return request