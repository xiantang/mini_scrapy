import unittest

from mini_scrapy.core.start_spider import init_spider
# from mini_scrapy.test_spider.test import TestSpider


class TeseFunc(unittest.TestCase):

    def test_class_method(self):
        c = init_spider(TestSpider)
        self.assertEqual(c.spider.integer,1)


    def test_process_item(self):
        sql = """
                select *
                from table 
                where id = 1"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()