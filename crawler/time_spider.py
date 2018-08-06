import re
from lxml import etree

import pymysql

from crawler import settings
from mini_scrapy import Request
from mini_scrapy import Spider
from mini_scrapy.untils import url_join
from mini_scrapy.untils.untils import logger


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
        cur.execute("""select itemid from raw_item_d
                      limit 1,100 """)
        fc = cur.fetchall()
        for i in fc:
            start_url = "https://www.nosetime.com/xiangshui/"+str(i[0])

            yield Request(url=start_url,
                          callback=self.get_blog_list,
                          meta={'item_id':i[0]})


    def get_blog_list(self,response):

        perfumer_html_list=re.findall("调香师：(.*?)<br />",response.text)
        if len(perfumer_html_list) != 0:
            perfumer_html=perfumer_html_list[0]
            selector = etree.HTML(perfumer_html)
            perfumers = ','.join(selector.xpath('//a/text()'))
            print(perfumers)
            #
            # host = settings.MYSQL_HOST
            # db = settings.MYSQL_DBNAME
            # user = settings.MYSQL_USER
            # password = settings.MYSQL_PASSWORD
            # conn = pymysql.connect(host=host, db=db, user=user, password=password)
            # sql = """
            # update
            # raw_item_d
            # set
            # perfumers = '%s'
            # where
            # itemid = '%s'
            # """%(perfumers,response.meta['item_id'])
            # try:
            #     conn.cursor().execute(sql)
            #     conn.commit()
            #     logger.info("insert OK!"+str(perfumers))
            # except Exception as e:
            #     logger.error("Error: %s", str(e), exc_info=True)
