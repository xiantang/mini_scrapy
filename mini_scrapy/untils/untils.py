import hashlib
import inspect
import logging
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, urlsplit
from mini_scrapy.http.response import Response


def get_logger(name):
    default_logger = logging.getLogger(name)
    default_logger.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    stream.setFormatter(formatter)
    default_logger.addHandler(stream)
    return default_logger


logger = get_logger("myLogger")


def request_fingerprint(request):
    # print(request.url)
    scheme, netloc, path, params, query, fragment = urlparse(request.url)
    # 处理一下 把参数位置不一样的哈希一下
    keyvals = parse_qsl(query)
    keyvals.sort()

    query = urlencode(keyvals)

    canonicalize_url = urlunparse((
        scheme, netloc.lower(), path, params, query, fragment)
    )

    fpr = hashlib.sha1()
    fpr.update(canonicalize_url.encode('utf-8'))
    return fpr.hexdigest()


def iter_children_classes(values, clazz):
    """
    判断是不是类，或者是不是子类，不能是DownloaderMiddleWare
    :param values:
    :param clazz:
    :return:
    """
    for obj in values:
        if inspect.isclass(obj) and issubclass(obj, clazz) and obj is not clazz:
            yield obj


def call_func(func, errback=None, callback=None, *args, **kwargs):
    """

    :param func:
    :param errback:
    :param callback:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        result = func(*args, **kwargs)

    except Exception as exc:
        # 异常回调函数
        if errback:
            errback(exc)
    else:
        if callback:
            result = callback(result)

        return result


def get_result_list(result:list)->list:
    if result is None:
        return []
    if isinstance(result, (dict, str)):
        return [result]
    if hasattr(result, "__iter__"):
        # 如果是生成器对象
        return result


def url_join(response: Response, suburl: str) -> str:
    """
    通过response对象来整合部分的url 使其合法
    :param response:
    :param suburl:
    :return:
    """
    response_url = response.url
    scheme,netloc,*surplus=urlsplit(response_url)
    pre_url = scheme + '://'+ netloc
    complete_url = pre_url + suburl
    return complete_url

if __name__ == '__main__':

    r=Response("https://blog.csdn.net/u010255818/article/details/52740671")
    print(url_join(r,"/w"))