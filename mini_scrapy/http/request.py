from pickle import dumps,loads
class Request(object):
    """
    Request
    """

    def __init__(self, url,method='GET', data=None,  callback=None, headers=None,
                 dont_filter=False, meta=None):
        self.url = url
        self.data = data
        self.method = method
        self.callback = callback
        self.headers = headers or {}

        self.dont_filter = dont_filter #不过滤
        self.meta = self._load_meta(meta)


    def copy(self, *args, **kwargs):
        for key in ['url', 'method', 'callback', 'headers', 'dont_filter',
                    'meta']:
            # 用于传给下一个对象
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def dumps(self):
        return dumps(self)

    def loads(self):
        return loads(self)

    def _load_meta(self,coustom_meta):
        """
        这里就给出两个特殊键
        一个是proxy一个是timeout
        :return:
        """

        meta = {"proxy":None,
                "download_timeout":None,
                "retry_count":0}
        if isinstance(coustom_meta,dict):
            meta.update(coustom_meta)
        return meta


    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__

if __name__ == '__main__':
    rq=Request("www.baidu.com",meta={"g":1})
    # a=rq.copy()
    # print(a.url)
    # dump_req = rq.dumps()
    # print(dump_req)
    # rq = loads(dump_req)
    # print(rq.callback)
    print(rq.meta['g'])