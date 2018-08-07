"""
# @File  : smellSpider.py
# @Author: xiantang
# @Date  : 03/08/18
# @Email :zhujingdi1998@gmail.com
# blog : zhanshengpipidi.cn/blog
# Github : github.com/xiantang
"""
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
import json
from crawler import settings
from mini_scrapy import Request
from mini_scrapy import Spider
from mini_scrapy.untils import url_join
from mini_scrapy.untils.untils import logger


class SmellSpider(Spider):
    name = "SmellSpider"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        host = crawler.settings['MYSQL_HOST']
        db = crawler.settings['MYSQL_DBNAME']
        user = crawler.settings['MYSQL_USER']
        password = crawler.settings['MYSQL_PASSWORD']
        conn = pymysql.connect(host=host, db=db, user=user, password=password)
        spider.conn = conn

        return spider

    def get_conn(self):
        host = self.crawler.settings['MYSQL_HOST']
        db = self.crawler.settings['MYSQL_DBNAME']
        user = self.crawler.settings['MYSQL_USER']
        password = self.crawler.settings['MYSQL_PASSWORD']
        conn = pymysql.connect(host=host, db=db, user=user, password=password)
        return conn

    def start_requests(self):
        cur = self.conn.cursor()
        cur.execute("""select itemid from raw_item_d where itemid not in(
                        select  distinct itemid
                      from raw_item_smell_layer_d)""")
        fc = cur.fetchall()
        print(fc)
        for i in fc:
            start_url = "http://www.zhanshengpipidi.cn/blog" + str(i[0])

            yield Request(url=start_url,
                          callback=self.get_blog_list,
                          meta={'item_id': i[0]},dont_filter=True)

    def get_blog_list(self, response):
        print(len(response.text))
#         response_dict = json.loads(response.text)
#         mainodors = response_dict['mainodor']
#         for mianodor in mainodors:
#             # print(mianodor)
#
#             sql = """
#             insert raw_item_smell_rank
# value('%s','%s','%s')""" % (response.meta['item_id'], mianodor['uoodor'], mianodor['cnt'])
#             try:
#                 conn = self.get_conn()
#                 conn.cursor().execute(sql)
#                 conn.commit()
#                 logger.info("insert OK!" + str(mianodor['uoodor']))
#             except Exception as e:
#                 logger.error("Error: %s", str(e), exc_info=True)
