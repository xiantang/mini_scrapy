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



        return spider



    def start_requests(self):

        for i in range(100):
            start_url = "https://developer.mozilla.org/zh-CN/docs/Learn/Getting_started_with_the_web/JavaScript_basics"

            yield Request(url=start_url,
                          callback=self.get_blog_list,
                          dont_filter=True)

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
