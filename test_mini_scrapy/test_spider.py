from mini_scrapy import Request
from mini_scrapy import Spider
from mini_scrapy.untils import url_join


class TestSpider(Spider):

    name = "TestSpider"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TestSpider, cls).from_crawler(crawler, *args, **kwargs)
        print(args)
        return spider

    def start_requests(self):
        start_url = "http://www.zhanshengpipidi.cn/blog/assortment/"
        yield Request(url=start_url,callback=self.get_blog_list)

    def get_blog_list(self,response):
        selector=response.xpath("//div[@class='row']/div[@class='col-md-6']")
        for sel in selector:
            for link in sel.xpath("./a/@href"):
                com_url = url_join(response,link)
                yield Request(url=com_url,callback=self.get_article)

    def get_article(self,response):
        print(response.xpath("//div[@class='col-md-11']/h1/text()"))
