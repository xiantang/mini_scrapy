class Request(object):
    """
    Request
    """

    def __init__(self, url, method='GET', callback=None, headers=None,
                 dont_filter=False, meta=None):
        self.url = url
        self.method = method
        self.callback = callback
        self.headers = headers or {}
        self.dont_filter = dont_filter
        self.meta = meta if meta else {}

    def copy(self, *args, **kwargs):
        for key in ['url', 'method', 'callback', 'headers', 'dont_filter',
                    'meta']:
            # 用于传给下一个对象
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__

if __name__ == '__main__':
    rq=Request("www.baidu.com")
    a=rq.copy()
    print(a.url)