import re
from lxml import etree

class Response(object):
    """
    Response
    """
    #TODO:需要整合re到上面去
    def __init__(self, url, status=200, headers=None,
                 body='', text='', request=None):
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.text = text
        self.request = request

    def copy(self, *args, **kwargs):
        for key in ['url', 'status', 'headers', 'body', 'request']:
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def __str__(self):
        return "<%d %s>" % (self.status, self.url)

    @property
    def selector(self):
        selector = etree.HTML(self.text)
        return selector

    def xpath(self, xpath_str: str) -> list:
        """
        :param xpath_str: xpath 表达式
        :return:
        """
        result_list = self.selector.xpath(xpath_str)
        return result_list

    __repr__ = __str__
