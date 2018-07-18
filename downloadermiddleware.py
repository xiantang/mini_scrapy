from collections import defaultdict

from http_.request import Request
from utils import iter_children_classes, call_func

class DownloaderMiddleware(object):

    """ DownloaderMiddleware iterface """

    pass

class DownloaderMiddlewareManager(object):

    def __init__(self,spider):
        self.settings = spider.settings
        self.methods = defaultdict(list)
        #创建一个默认值为[]的字典
        self.middlewares = self.load_middleware()
        for miw in self.middlewares:
            self._add_middleware(miw)

    def load_middleware(self):
        """
        加载middleware
        :return:
        """
        #FIXME:I don‘t know what globals().values() mean
        middlewares = []
        for miw in iter_children_classes(
            globals().values(),DownloaderMiddleware
        ):
            middlewares.append(miw(self.settings))
        return middlewares

    def _add_middleware(self,miw):
        if hasattr(miw,"process_request"):
            self.methods['process_request'].append(miw.process_request)
        if hasattr(miw,"process_response"):
            self.methods['process_response'].insert(0, miw.process_response)
        if hasattr(miw,"process_exception"):
            self.methods['process_exception'].insert(0,miw.process_exception)

    def download(self,download_func,request):
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
            return download_func(request)

        def process_response(response):
            for method in self.methods['prcess_response']:
                response = method(request,response)
                if isinstance(response,Request):
                    return  response

        def process_exception(exception):
            for method in self.methods['process_exception']:
                response = method(request,exception)
                if response:
                    return response
            return exception

        return call_func(process_request,process_exception,
                         process_response,request)