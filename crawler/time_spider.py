import pymysql

from mini_scrapy import Request
from mini_scrapy import Spider
from mini_scrapy.untils import url_join


class TimeSpider(Spider):

    name = "TestSpider"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TimeSpider, cls).from_crawler(crawler, *args, **kwargs)
        host = crawler.settings['MYSQL_HOST']
        db=crawler.settings['MYSQL_DBNAME']
        user=crawler.settings['MYSQL_USER']
        password=crawler.settings['MYSQL_PASSWORD']
        conn = pymysql.connect(host=host,db=db,user=user,password=password)
        spider.conn = conn
        return spider

    def start_requests(self):
        cur = self.conn.cursor()
        cur.execute("""select itemid from raw_item_d""")
        fc = cur.fetchall()
        for i in fc:
            start_url = "https://www.nosetime.com/xiangshui/"+str(i[0])

            yield Request(url=start_url,
                          callback=self.get_blog_list,
                          meta={'item_id':i[0]})


    def get_blog_list(self,response):
       print(len(response.text))
       print(response.meta['item_id'])