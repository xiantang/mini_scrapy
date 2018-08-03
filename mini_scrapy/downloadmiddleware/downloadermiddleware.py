from collections import defaultdict

from scrapy.utils.misc import load_object

from mini_scrapy.http.request import Request
from mini_scrapy.untils.untils import iter_children_classes, call_func


class DownloaderMiddleware(object):
    """ DownloaderMiddleware iterface """

    def __init__(self,spider,crawler,**kwargs):
        self.spider = spider
        self.cralwer = crawler

    @classmethod
    def from_crawler(cls, spider, crawler, **kwargs):
        cls(spider,crawler,**kwargs)

    def process_request(self,request):
        return  request

    def process_response(self,request,response):
        return  response

    def process_exception(self,request,exception):
        return exception

class DownloaderMiddlewareManager(object):

    def __init__(self, spider,crawler,settings):
        self.settings = settings
        self.methods = defaultdict(list)
        self.spider = spider
        self.crawler = crawler
        # 创建一个默认值为[]的字典
        self.middlewares = self._load_middleware()
        for miw in self.middlewares:
            self._add_middleware(miw)

    @classmethod
    def from_crawler(cls,spider,crawler,**kwargs):
        settings = crawler.settings
        return  cls(spider,crawler,settings)


    def _load_middleware(self):
        """
        加载middleware

        :return:
        """
        # FIXME:重写 从settings 中加载中间件
        # TODO:need to rewrite !
        # middlewares = []
        # # print(globals())
        # for miw in iter_children_classes(globals().values(), DownloaderMiddleware):
        #     middlewares.append(miw(self.settings))
        # return middlewares
        middlewares = []
        middlewares_dict = self.settings["DOWNLOAD_MIDDLEWARE"]
        middlewares_list=sorted(middlewares_dict.items(), key=lambda x: x[1])
        #对字典中序列根据value排序
        for middleware_key,value in middlewares_list:

            middleware = load_object(middleware_key)
            if  issubclass(middleware,DownloaderMiddleware):
                if hasattr(middleware,"from_crawler"):
                    middleware_instance = middleware.from_crawler(self.spider,self.crawler)
                    middlewares.append(middleware_instance)
                else:
                    middleware_instance = middleware()
                    middlewares.append(middleware_instance)
        return middlewares
    def _add_middleware(self, miw):
        if hasattr(miw, "process_request"):
            self.methods['process_request'].append(miw.process_request)
        if hasattr(miw, "process_response"):
            self.methods['process_response'].insert(0, miw.process_response)
        if hasattr(miw, "process_exception"):
            self.methods['process_exception'].insert(0, miw.process_exception)

    def download(self, download_func, request):
        """
        call func process_request 第一个参数是fuc
                  process_response callback

        :param download_func:fetch
        :param request:
        :return:
        """

        def process_request(request):
            for method in self.methods['process_request']:
                method(request)
            response = download_func(request)
            # if response is None:
            #     print(1)
            #     print(1)

            return response

        def process_response(response):

            for method in self.methods['process_response']:

                response = method(request, response)
                if isinstance(response, Request):
                    return response
                # 解决了一个bug return 放在上一级
            return response

        def process_exception(exception):
            for method in self.methods['process_exception']:
                response = method(request, exception)
                if response:
                    return response
            return exception

        # print(self.methods)
        resp = call_func(process_request, process_exception,
                  process_response, request)

        return resp


class RetryMiddleware(DownloaderMiddleware):
    RETRY_EXCEPTIONS = ()

    def __init__(self, spider,crawler,settings):
        super().__init__(spider,crawler)
        self.max_retry_count = settings.get_int("RETRY_COUNT")
        self.retry_status_codes = settings.get_list("RETRY_STATUS_CODES")

    @classmethod
    def from_crawler(cls,spider,crawler,**kwargs):
        settings = crawler.settings
        return cls(spider,crawler,settings)


    def process_response(self, request, response):
        """process respoonse
        """
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_status_codes:
            return self._retry(request) or response
        return response

    def process_exception(self, request, exception):
        """process exception
        """
        if isinstance(exception, self.RETRY_EXCEPTIONS) \
                and request.meta.get("dont_retry", False):
            return self._retry(request)

    def _retry(self, request):
        """retry
        """
        retry_count = request.meta.get("retry_count", 0) + 1
        if retry_count <= self.max_retry_count:
            retry_request = request.copy()
            retry_request.meta["retry_count"] = retry_count
            return retry_request
