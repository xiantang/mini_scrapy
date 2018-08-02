"""
# @File  : review_spider.py
# @Author: xiantang
# @Date  : 01/08/18
# @Email :zhujingdi1998@gmail.com
# blog : zhanshengpipidi.cn/blog
# Github : github.com/xiantang
"""
import re
from lxml import etree

import pymysql

from crawler import settings
from mini_scrapy import Request
from mini_scrapy import Spider
from mini_scrapy.untils import url_join
from mini_scrapy.untils.untils import logger


class ReviewSpider(Spider):

    name = "TestSpider"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ReviewSpider, cls).from_crawler(crawler, *args, **kwargs)
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
                        """)
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

            brand = response.xpath("//ul[@class='item_info']/li/a[1]/@href")[0]
            url = url_join(response,brand)

            yield Request(url=url,callback=self.brand)

    def brand(self,response):
        # print(len(response.text))
        pass