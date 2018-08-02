""" default config settings """

RETRY_COUNT = 3

RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

TIMEOUT = 30

DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
}


MAX_REQUEST_SIZE = 20

COOKIE_ENABLE = True

PROXY_INTERVAL = 5

SCHEDULER_PATH = "mini_scrapy.core.scheduler.Scheduler"

DOWNLOADER_PATH = "mini_scrapy.downloadmiddleware.downloader.Downloader"

DUPEFILTER = "mini_scrapy.core.dupefilters.RFPDupeFilter"

BLOOMFILTER_SIZE = 10000

BLOOMFILTER_HASH_COUNT = 10

USER_AGENT = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}