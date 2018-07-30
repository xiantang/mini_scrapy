import re
import unittest
from unittest import TestCase
from scrapy.utils.misc import load_object
from mini_scrapy.core.engine import Engine
from mini_scrapy.http.response import Response
from mini_scrapy.untils import url_join


class TeseFunc(TestCase):

    def is_url(self,url):
        """
        判断url是否合法
        :param url:
        :return:
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        matched = re.match(regex,url)
        return False if matched is None else True

    def test_url_join(self):
        """
        测试url_join
        :return:
        """
        r = Response("https://blog.csdn.net/u010255818/article/details/52740671")
        sub_url = '/u010255818'
        com_url = url_join(r,sub_url)

        self.assertTrue(self.is_url(com_url))


    def test_load_object(self):
        path = "mini_scrapy.core.engine.Engine"
        cls = load_object(path)

        self.assertTrue(Engine is cls)

if __name__ == '__main__':
    unittest.main()